import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="assart",
    version="0.2.0",
    url="https://github.com/mmcclellan/assart",
    license='MIT',
    author="Michael McClellan",
    author_email="mcclellan.m@gmail.com",
    description="A simple s3 analytics reporting tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["boto3"],
    entry_points={
        "console_scripts": ["assart=assart.__main__:main"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
