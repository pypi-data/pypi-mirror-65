import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nomnomdata-engine",
    version="0.1.1",
    author="Nom Nom Data Inc",
    author_email="info@nomnomdata.com",
    description="Package containing tooling for developing nominode engines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/nomnomdata/tools/nomnomdata-engine",
    packages=setuptools.find_namespace_packages(),
    classifiers=["Programming Language :: Python :: 3.7"],
    install_requires=[
        "requests>=2.6.1",
        "pytest>=3.8.0",
        "pytest-cov>=2.6.0",
        "httmock>=1.2.6",
        "nomnomdata-cli>=0.1.0",
    ],
    entry_points={"nomnomdata.cli_plugins": {"engine=nomnomdata.engine.cli:cli"}},
    python_requires=">=3.7",
    zip_safe=False,
)
