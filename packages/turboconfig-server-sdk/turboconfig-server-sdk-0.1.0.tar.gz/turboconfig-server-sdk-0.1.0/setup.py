from setuptools import find_packages, setup


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


install_reqs = parse_requirements("requirements.txt")
reqs = [ir for ir in install_reqs]

setup(
    name="turboconfig-server-sdk",
    version="0.1.0",
    author="TurboConfig",
    author_email="garg95hitesh@gmail.com",
    packages=find_packages(),
    url="https://gitlab.com/indusbit/turboconfig-python",
    description="TurboConfig SDK for Python",
    long_description="TurboConfig SDK for Python",
    install_requires=reqs,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
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
