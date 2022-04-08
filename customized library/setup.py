import setuptools

setuptools.setup (
    name = "customlib",
    version = "0.1",
    # metadata for upload to PyPI
    author = "Andy Pham",
    author_email = "aqpham02@gmail.com",
    description = "This is a configuration directory Package",
    url="",
    packages = setuptools.find_packages(),
    python_requires = '>=3.6'
)