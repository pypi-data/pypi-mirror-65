import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk8s",
    "version": "0.18.0",
    "description": "Cloud Development Kit for Kubernetes",
    "license": "Apache-2.0",
    "url": "https://github.com/awslabs/cdk8s",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "project_urls": {
        "Source": "https://github.com/awslabs/cdk8s.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk8s",
        "cdk8s._jsii"
    ],
    "package_data": {
        "cdk8s._jsii": [
            "cdk8s@0.18.0.jsii.tgz"
        ],
        "cdk8s": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=1.1.0",
        "publication>=0.0.3",
        "constructs>=2.0.1, <3.0.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
