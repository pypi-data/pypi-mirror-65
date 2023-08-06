#!/usr/bin/env python3

import re
import setuptools

with open("fdbk_dynamodb_plugin/_version.py", "r") as f:
    try:
        version = re.search(
            r"__version__\s*=\s*[\"']([^\"']+)[\"']",f.read()).group(1)
    except:
        raise RuntimeError('Version info not available')

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="fdbk_dynamodb_plugin",
    version=version,
    author="Toni Kangas",
    description="DynamoDB plugin for fdbk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kangasta/fdbk_dynamodb_plugin",
    packages=setuptools.find_packages(),
    install_requires=[
        "fdbk==2.0a3",
        "boto3>=1.12.33"
    ],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
