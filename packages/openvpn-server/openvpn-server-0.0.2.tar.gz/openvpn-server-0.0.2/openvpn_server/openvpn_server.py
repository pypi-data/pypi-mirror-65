import getpass
import logging
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import ByteString, Optional, Type
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
        **kwargs: dict,
    ):
        self.config = {}
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
        config.config["management"] = f"{self._mgmt_socket} unix"  # type: ignore
        config.config["management-client-user"] = getpass.getuser()  # type: ignore  # TODO check if it works

        config_handle = self._runtime_dir / "config"
        config_handle.write_bytes(config.get_content())
        self._start_ovpn(
            config_path=config_handle.as_posix(), openvpn_binary=openvpn_binary, privesc_binary=privesc_binary
        )

        self._mgmt = openvpn_api.VPN(socket=self._mgmt_socket.as_posix())

    def _start_ovpn(self, config_path: str, openvpn_binary: str, privesc_binary: Optional[str]) -> None:
        command = []
        if privesc_binary is not None:
            command.append(privesc_binary)
        command.extend([openvpn_binary, config_path])
        logger.debug("Spawning process %s", command)
        self._proc = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self._runtime_dir.as_posix()
        )  # TODO check stdout for service readiness
        logger.debug("Process spawned, PID %s", self._proc.pid)
        time.sleep(1)  # TODO make it smarter

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
            self._mgmt.send_command("signal SIGTERM")
        self._stdout, self._stderr = self._proc.communicate()

    @property
    def is_running(self) -> bool:
        return self._mgmt_socket.exists()

    @property
    def stdout(self) -> ByteString:
        self._stdout, self._stderr = self._proc.communicate(timeout=0.01)
        return self._stdout

    @property
    def stderr(self) -> ByteString:
        self._stdout, self._stderr = self._proc.communicate(timeout=0.01)
        return self._stderr
