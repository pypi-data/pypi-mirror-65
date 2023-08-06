import setuptools  # type: ignore
from pathlib import Path

DEV_REQUIREMENTS = ["tox==3.14.5"]
TEST_REQUIREMENTS = [
    "black==19.10b0",
    "flake8==3.7.*",
    "flake8-bugbear==19.8.0",
    "mypy==0.770",
    "pytest==5.4.1",
]

setuptools.setup(
    name="openvpn-server",
    use_scm_version=True,
    author="Piotr Szczepaniak",
    author_email="szczep.piotr+openvpn-server@gmail.com",
    description="Python package for managing OpenVPN instances through their entire life cycle",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/D0han/openvpn-server",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Topic :: System :: Networking",
    ],
    setup_requires=["setuptools_scm", "openvpn_api"],  # TODO in reality we need openvpn_api>0.1.3
    extras_require={"dev": DEV_REQUIREMENTS + TEST_REQUIREMENTS, "testing": TEST_REQUIREMENTS},
    python_requires=">=3.6.0",
)
