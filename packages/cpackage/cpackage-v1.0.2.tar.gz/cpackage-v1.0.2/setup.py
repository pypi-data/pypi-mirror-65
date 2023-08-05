from distutils.core import setup

setup(
    name="cpackage",
    packages=["cpackage"],
    version="v1.0.2",
    license="MIT",
    description="""A python utility for creating better modules/packages.
    This module give the ability to quickly create and add files to different directories.
    From creating directory & sub directory to managing the files that are put into those folders.
    This is more of an automation tool for writing modules but can be used for other package related matters.""",
    author="Cru1seControl",
    author_email="Cru1seControl.loot@gmail.com",
    url="https://github.com/Cru1seControl",
    download_url="https://github.com/Cru1seControl/python-cpackage",
    keywords=["packaging", "filesystem", "tool"],
    classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.6"
    ]

)
