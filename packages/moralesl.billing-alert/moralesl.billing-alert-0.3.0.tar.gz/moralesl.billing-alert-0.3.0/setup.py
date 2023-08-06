import json
import setuptools

kwargs = json.loads("""
{
    "name": "moralesl.billing-alert",
    "version": "0.3.0",
    "description": "Utility CDK construct to setup billing alerts easily",
    "license": "MIT",
    "url": "https://github.com/moralesl/cdk-billing-alert.git",
    "long_description_content_type": "text/markdown",
    "author": "Luis Morales",
    "project_urls": {
        "Source": "https://github.com/moralesl/cdk-billing-alert.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "moralesl.billing_alert",
        "moralesl.billing_alert._jsii"
    ],
    "package_data": {
        "moralesl.billing_alert._jsii": [
            "billing-alert@0.3.0.jsii.tgz"
        ],
        "moralesl.billing_alert": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=1.2.0",
        "publication>=0.0.3",
        "aws-cdk.aws-cloudwatch==1.32.2",
        "aws-cdk.aws-cloudwatch-actions==1.32.2",
        "aws-cdk.aws-sns==1.32.2",
        "aws-cdk.aws-sns-subscriptions==1.32.2",
        "aws-cdk.core==1.32.2",
        "constructs>=2.0.0, <3.0.0"
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
