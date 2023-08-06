import setuptools


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setuptools.setup(
    name="playment",
    version="1.0.3",
    description="A Python package to interact with Playment's APIs.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/crowdflux/playment-sdk-python.git",
    author="Playment",
    author_email="dev@playment.in",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    keywords=["playment"],
)
