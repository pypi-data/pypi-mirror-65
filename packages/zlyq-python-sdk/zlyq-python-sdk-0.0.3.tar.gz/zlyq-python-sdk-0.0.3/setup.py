from setuptools import setup, find_packages

setup(
    name = "zlyq-python-sdk",
    version = "0.0.3",
    keywords = ("pip", "pathtool","timetool", "magetool", "mage"),
    description = "data synchronization tools for zlyq service",
    long_description = "data synchronization tools for zlyq service, for now including user data, content data and user history data",
    license = "MIT Licence",

    url = "https://github.com/zlzz-rec/zlyq-python-sdk",
    author = "Clifford",
    author_email = "290416118@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)
