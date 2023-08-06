from setuptools import setup
from pathlib import Path

GEN_version = "0.0.3"
READ_name = "notiforward"

here = Path(__file__).parent.resolve()

setup(
    name=READ_name,
    version=GEN_version,
    author="rendaw",
    url="https://gitlab.com/rendaw/notiforward",
    download_url="https://gitlab.com/rendaw/notiforward/-/archive/v{v}/notiforward-v{v}.tar.gz".format(
        v=GEN_version
    ),
    license="MIT",
    description="Forward DBUS notifications",
    long_description=(here / "README.md").read_text(),
    long_description_content_type="text/markdown",
    classifiers=[],
    py_modules=["notiforward"],
    install_requires=["dbus-python==1.2.16", "pygobject==3.36.0", "requests==2.23.0",],
    entry_points={"console_scripts": ["notiforward=notiforward:main"]},
)
