import setuptools

setuptools.setup(
    name="dynamodb-traverse",
    version="0.1.7",
    description="High performance, thread safe traversing tool for AWS DynamoDB",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # The project's main homepage.
    url="https://github.com/holyshipt/dynamodb-traverse",
    # Author details
    author="Lawrence He",
    author_email="ruyangmao1001@gmail.com",
    # Choose your license
    license="Apache License 2.0",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.8",
    ],
    # packages=setuptools.find_packages(),
    packages=["dynamodb-traverse"],
    python_requires=">=3.8",
)
