from setuptools import setup

with open("VERSION.txt", "r") as f:
    __version__ = f.read().strip()

with open('development_requirements.txt') as f:
    dev_requirements = f.read().splitlines()

NAME = "mitiq"
AUTHOR = "Ryan LaRose, Andrea Mari, Nathan Shammah, Will Zeng"
URL = "https://github.com/unitaryfund"
LICENSE = "GPL v3.0"
setup(
    name=NAME,
    version=__version__,
    packages = ['mitiq'],
    install_requires=['numpy>=1.18.1'],
    dev_requirements={'pytest>=5.4.1'},
    author=AUTHOR,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url = URL,
   classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows"
        ],
    license = LICENSE
)
