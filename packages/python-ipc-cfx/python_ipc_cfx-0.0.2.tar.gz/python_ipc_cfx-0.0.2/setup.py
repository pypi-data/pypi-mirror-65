"""Setup file for python_ipc_cfx"""

from setuptools import setup, find_packages
import version

setup(
    name="python_ipc_cfx",
    packages=find_packages(exclude=("test",)),
    version=version.version,
    license="proprietary",
    install_requires=[
        "python-dateutil>=2.8.0",
        "pytz>=2019.2",
        "stringcase>=1.2.0"
    ],
    tests_require=[
        'pytest',
        'tox'
    ],
    entry_points={
    },
    include_package_data=True,
    description="Python implementation of the IPC-CFX standard",
    author="Arch",
    author_email="info@archsys.io",
    url="https://github.com/iotile/python-ipc-cfx",
    keywords=["iotile", "arch", "industrial"],
    python_requires=">=3.5, <4",
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules"
        ],
    long_description="""\
Python IPC-CFX
--------------------------

Python implementation of the IPC-CFX standard.

http://www.connectedfactoryexchange.com/CFXDemo/sdk/html/R_Project_CFXSDK.htm

See https://www.archsys.io
"""
)
