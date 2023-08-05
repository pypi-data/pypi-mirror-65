from setuptools import setup, find_packages


with open("pypi_readme.md", "r") as readme:
    long_description = readme.read()

setup(
    name="autoconfiguration",
    version="0.2",
    author="Konstantin Müller",
    author_email="konstantin.mueller.dev@gmail.com",
    description="Load configuration files (.ini) automatically",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/konstantin-mueller/python-autoconfiguration",
    download_url="https://gitlab.com/konstantin-mueller/python-autoconfiguration",
    project_urls={
        "repository": "https://gitlab.com/konstantin-mueller/python-autoconfiguration",
        "bugs": "https://gitlab.com/konstantin-mueller/python-autoconfiguration/issues",
    },
    license="Apache License 2.0",
    packages=find_packages(),
    package_data={"": ["LICENSE", "README.md",], "autoconfiguration": ["*.*",],},
    include_package_data=True,
    classifiers=[
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
)
