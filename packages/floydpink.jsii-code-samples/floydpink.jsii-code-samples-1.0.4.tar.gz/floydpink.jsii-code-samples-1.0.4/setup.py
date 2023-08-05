import json
import setuptools

kwargs = json.loads("""
{
    "name": "floydpink.jsii-code-samples",
    "version": "1.0.4",
    "description": "Code samples that accompany the AWS blog post on jsii",
    "license": "MIT",
    "url": "https://github.com/jsii-code-samples/jsii-code-samples#readme",
    "long_description_content_type": "text/markdown",
    "author": "Hari Pachuveetil <pachuvee@amazon.com>",
    "project_urls": {
        "Source": "https://github.com/jsii-code-samples/jsii-code-samples.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "floydpink.jsii_code_samples",
        "floydpink.jsii_code_samples._jsii"
    ],
    "package_data": {
        "floydpink.jsii_code_samples._jsii": [
            "jsii-code-samples@1.0.4.jsii.tgz"
        ],
        "floydpink.jsii_code_samples": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=1.1.0",
        "publication>=0.0.3"
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
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
