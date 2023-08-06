import setuptools
from setuptools import setup

# without tensorflow by default
install_requires = [
    "numpy",
    "requests",
    "flask",
    "scikit-learn",
    "jsonlines",
    "pconf",
    "tokenizer_tools",
    "tf_summary_reader",
    "tensorflow>=1.15.0,<2.0.0"
]


setup(
    name="ioflow",
    version="0.10.0",
    packages=setuptools.find_packages(),
    url="https://github.com/howl-anderson/ioflow",
    license="Apache 2.0",
    author="Xiaoquan Kong",
    author_email="u1mail2me@gmail.com",
    description="Input/Output abstraction layer for machine learning",
    install_requires=install_requires,
    tests_require=["requests-mock", "pytest", "pytest-datadir"],
)
