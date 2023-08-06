from setuptools import setup
from setuptools import find_packages

__version__ = '0.0.1'


def long_description():
    with open('README.md') as fp:
        return fp.read()


def get_requirements():
    with open("requirements.txt") as fp:
        dependencies = (d.strip() for d in fp.read().split("\n") if d.strip())
        return [d for d in dependencies if not d.startswith("#")]


setup(
    name="teardrop",
    version=f"{__version__}.dev1",
    description="A Python algorithms used to perform machine learning.",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author="Dec0Ded",
    author_email="teardropemail@gmail.com",
    license="LGPL-3.0-ONLY",
    url="https://gitlab.com/michkaro/teardrop",
    python_requires="> 3.7",
    install_requires=get_requirements(),
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
