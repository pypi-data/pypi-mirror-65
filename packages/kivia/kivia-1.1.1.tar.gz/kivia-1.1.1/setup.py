from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.MD')) as f:
    long_description = f.read()

setup(
    name="kivia",
    version="1.1.1",
    description="A python cli which solves every problem in cli.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/wisdomrider/kivia-cli",
    author="wisdomrider",
    author_email="avishekzone@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["kivia"],
    include_package_data=True,
    install_requires=["click", "colorama", "requests", "sqliteclosedhelper"],
    entry_points={
        "console_scripts": [
            "kpm=kivia.app:startUp",
        ]
    },
)
