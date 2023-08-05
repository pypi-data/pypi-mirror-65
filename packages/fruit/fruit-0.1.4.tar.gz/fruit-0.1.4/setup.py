from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="fruit",
    version="0.1.4",
    packages=find_packages(),
    install_requires=['click', 'colorama', 'pyyaml', 'checksumdir'],
    entry_points={
        'console_scripts': ['fruit=fruit.fruit:cli'],
    },
    author="Marcell Pigniczki",
    author_email="marcip97@gmail.com",
    description="Create and run automations based on yaml files",
    long_description=read('readme.rst'),
    license="MIT",
    keywords="fruit automation yaml",
    url="https://github.com/codesaurus97/fruit",
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
        ],
    zip_safe=False,
    package_data={"fruit": ["__init__.py"]},
    python_requires='>=3.6',
)
