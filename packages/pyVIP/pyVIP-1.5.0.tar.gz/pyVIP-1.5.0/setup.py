import setuptools
import virtualitics

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyVIP",
    version=virtualitics.__version__,
    author="Virtualitics",
    author_email="aakash@virtualitics.com",
    description="Python API for VIP (Virtualitics Immersive Platform)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "License :: OSI Approved :: MIT License"
    ],
    license="MIT LICENSE"
)
