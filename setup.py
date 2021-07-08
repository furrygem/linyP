from setuptools import setup
import setuptools

setup(
    name = "linyP",
    version = '1.0',
    url = "https://github.com/furrygem/linyP",
    description = "multiline progress display",
    long_description = open("docs.md", "r").read(),
    long_description_content_type = 'text/markdown',
    author = "furrygem",
    maintainer = "furrygem",
    packages=["linyP"]
)
