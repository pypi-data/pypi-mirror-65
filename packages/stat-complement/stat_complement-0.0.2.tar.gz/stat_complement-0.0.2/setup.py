import setuptools
from os import path

DIR=path.dirname(path.abspath(__file__))
with open(path.join(DIR,'requirements.txt')) as f:
    INSTALL_PACKAGES=f.read().splitlines()

with open(path.join(DIR,'README.md')) as f:
    README=f.read()

setuptools.setup(
    name="stat_complement",
    version="0.0.2",
    author="jameslahm",
    description="A package as a complement for statistic computation",
    long_description=README,
    long_description_content_type='text/markdown',
    url="http://github.com/jameslahm/stat_complement",
    install_requires=INSTALL_PACKAGES,
    author_email="wa17@mails.tsinghua.edu.cn",
    keywords=['statistic']
)