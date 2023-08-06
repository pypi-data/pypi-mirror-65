from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'helloworld_xiaoyanli',
    version='0.0.1',
    description='say hello!',
    py_modules=["helloworld_xiaoyanli629"],
    package_dir = {'': 'src'},

    long_description=long_description,
    long_description_content_type = "text/markdown",

    url = "https://github.com/xiaoyanLi629",
    author = "Xiaoyan Li",
    author_email="xiaoyanli629@gmail.com",

)