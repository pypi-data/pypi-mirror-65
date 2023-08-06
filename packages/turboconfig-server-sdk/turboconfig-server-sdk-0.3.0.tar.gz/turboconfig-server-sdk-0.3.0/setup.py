from setuptools import find_packages, setup

VERSION = "0.3.0"

setup(
    name="turboconfig-server-sdk",
    version=VERSION,
    author="TurboConfig",
    author_email="garg95hitesh@gmail.com",
    packages=find_packages(),
    url="https://gitlab.com/indusbit/turboconfig-python",
    description="TurboConfig SDK for Python",
    long_description="TurboConfig SDK for Python",
    install_requires=["requests"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
    ],
)
