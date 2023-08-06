# author: EasyCV Developers
# -*- coding: utf-8 -*-

from setuptools import setup


# Get the long description from the README file
with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="easycv",
    packages=["easycv"],
    version="0.1.1",
    license="MIT",
    description="Computer Vision made easy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="EasyCV Developers",
    author_email="easycv.developers@gmail.com",
    url="https://github.com/easycv/easycv",
    download_url="https://github.com/easycv/easycv/archive/v0.1.1.tar.gz",
    keywords=["easycv", "computer vision", "python", "ai"],
    setup_requires=["setuptools>=38.6.0"],
    install_requires=[
        "numpy",
        "pillow",
        "requests",
        "scipy",
        "matplotlib",
        "opencv-python",
        "scikit-image",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
