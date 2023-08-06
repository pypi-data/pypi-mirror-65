import datetime
import getpass
import logging
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import ByteString, Optional, Type, Dict
from types import TracebackType

import openvpn_api  # type: ignore

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OpenVPNConfig:
    def __init__(
        self,
        ca: Optional[str] = None,
        cert: Optional[str] = None,
        key: Optional[str] = None,
        dh: Optional[str] = None,
        **kwargs: str,
    ):
        self.config: Dict[str, str] = {}
        self.config.update(kwargs)
        self.ca = ca
        self.cert = cert
        self.key = key
        self.dh = dh

    def get_content(self) -> bytes:
        generated = "\n".join(f"{key} {value}" for key, value in self.config.items())
        generated += "\n"
        generated += "".join(self._inline(option) for option in ("ca", "cert", "key", "dh"))
        return generated.encode()

    def _inline(self, option_name: str) -> str:
        option_content = self.__getattribute__(option_name)
        if option_content:
            return f"<{option_name}>\n{option_content}\n</{option_name}>\n"
        return ""


class OpenVPNServer:
    def __init__(
        self,
        config: OpenVPNConfig,
        openvpn_binary: str = "openvpn",
        runtime_base_dir: Optional[Path] = None,
        privesc_binary: Optional[str] = "sudo",
        startup_timeout: int = 2,
    ):
        self._stdout: ByteString = b""
        self._stderr: ByteString = b""
        self._exit_code: Optional[int] = None

        if runtime_base_dir is None:
            runtime_base_dir = Path(tempfile.gettempdir()) / "python-openvpn-{}".format(os.getuid())
            logger.warning(f"runtime_dir not set, defaulting to {runtime_base_dir}")
        runtime_base_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        self._runtime_dir = Path(tempfile.mkdtemp(dir=runtime_base_dir))
        logger.info(f"Using {self._runtime_dir} to store runtime objects")

        self._mgmt_socket = self._runtime_dir / "ovpn.sock"
        config.config["management"] = f"{self._mgmt_socket} unix"
        config.config["management-client-user"] = getpass.getuser()

        config_handle = self._runtime_dir / "config"
        config_handle.write_bytes(config.get_content())
        self._start_ovpn(
            config_path=config_handle.as_posix(), openvpn_binary=openvpn_binary, privesc_binary=privesc_binary
        )

        self._mgmt = openvpn_api.VPN(socket=self._mgmt_socket.as_posix())
        if not self._stall_until_ovpn_ready(timeout=startup_timeout):
            raise SystemError

    def _start_ovpn(self, config_path: str, openvpn_binary: str, privesc_binary: Optional[str]) -> None:
        command = []
        if privesc_binary is not None:
            command.append(privesc_binary)
        command.extend([openvpn_binary, config_path])
        logger.debug("Spawning process %s", command)
        self._proc = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self._runtime_dir.as_posix()
        )
        logger.debug("Process spawned, PID %s", self._proc.pid)

    def _stall_until_ovpn_ready(self, timeout: int) -> bool:
        timestamp_end = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        while datetime.datetime.now() < timestamp_end:
            self._mgmt.clear_cache()
            if self.is_running:
                try:
                    with self._mgmt.connection():
                        state = self._mgmt.state
                        if state.state_name == "CONNECTED":
                            return True
                        logger.debug(state.state_name)
                except openvpn_api.util.errors.ConnectError as e:
                    logger.debug(e)
                    stdout, _ = self._proc.communicate(timeout=0.01)
                    logger.debug(stdout.decode())
                    if b"Exiting due to fatal error" in stdout:
                        break
            time.sleep(0.1)
        return False

    def __enter__(self) -> "OpenVPNServer":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
    ) -> None:
        self.stop()

    def stop(self) -> None:
        if not self.is_running:
            return
        with self._mgmt.connection():
            self._mgmt.send_sigterm()
        timestamp_end = datetime.datetime.now() + datetime.timedelta(seconds=5)
        while datetime.datetime.now() < timestamp_end:
            if not self.is_running:
                return
            time.sleep(0.1)
        raise SystemError

    @property
    def is_running(self) -> bool:
        return self._mgmt_socket.exists()
