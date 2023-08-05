import setuptools

pkg_version = "0.1.8"

setuptools.setup(
    name="fastg2protlib",
    version=f"{pkg_version}",
    packages=["fastg2protlib"],
    install_requires=["biopython", "lxml", "networkx", "numpy", "pyteomics",],
    description="FASTG sequences to a protein library",
    author="Thomas McGowan",
    author_email="mcgo0092@umn.edu",
    url="https://github.umn.edu/mcgo0092/fastg2protlib.git",
    download_url=f"https://github.umn.edu/mcgo0092/fastg2protlib/archive/v_{pkg_version}.tar.gz",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
