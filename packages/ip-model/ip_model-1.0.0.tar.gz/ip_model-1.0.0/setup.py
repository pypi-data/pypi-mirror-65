from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="ip_model",
    version="1.0.0",
    description="A Python package for storing, removing and checking IP's efficiently,"
                " Use cases: Blacklisting, Whitelisting etc",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/rakesht2499/Ip-Model",
    author="Rakesh Kumar T",
    author_email="rakesht2499@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["ip_model"],
    include_package_data=True,
    install_requires=[],
    entry_points={},
)
