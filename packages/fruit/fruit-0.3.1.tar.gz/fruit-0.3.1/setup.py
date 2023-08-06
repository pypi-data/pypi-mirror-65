from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="fruit",
    version="0.3.1 ",
    packages=find_packages(),
    install_requires=['click', 'colorama', 'tabulate', 'questionary'],
    entry_points={
        'console_scripts': ['fruit=fruit.fruit:main'],
    },
    author="Marcell Pigniczki",
    author_email="marcip97@gmail.com",
    description="Create and run automations python scripts",
    long_description=read('readme.rst'),
    license="MIT",
    keywords="fruit, automation, python",
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
