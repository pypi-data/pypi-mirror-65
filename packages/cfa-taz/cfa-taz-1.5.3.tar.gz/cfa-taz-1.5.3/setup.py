from setuptools import setup, find_packages
import os
from taz._version import __version__

long_description = "SEE README file"

setup(
    name="cfa-taz",  # name your package
    packages=find_packages(exclude=["tests/config.py"]),
    version=__version__,
    description="High level API for azure",
    long_description=long_description,
    package_dir={"taz": "taz"},
    author="Christophe Fauchard",
    author_email="christophe.fauchard@gmail.com",
    license="MIT",  # MIT, GPL, BSD ??
    install_requires=[
        "pandas>=0.25.3",
        "azure-common>=1.1.25",
        "msrestazure>=0.6.3",
        "adal>=1.2.2",
        "azure-cli-core>=2.3.1",
        "azure-mgmt-containerinstance>=1.5.0",
        "azure-mgmt-msi>=1.0.0",
        "azure-mgmt-containerregistry>=2.8.0",
        "azure-storage-common>=2.1.0",
        "azure-storage-blob>=12.3.0",
        "azure-datalake-store>=0.0.48",
        "azure-keyvault-secrets>=4.1.0",
        "azure-identity>=1.3.0",
    ],
)
