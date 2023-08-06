from setuptools import setup, find_packages

with open("README.md") as fp:
    long_description = fp.read()

setup(
    name='hcdk_eks',
    version='0.0.3',

    description="EKS library for the Halloumi modules of the AWS CDK",
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        "aws-cdk.aws-autoscaling",
        "aws-cdk.aws-ec2",
        "aws-cdk.aws-eks",
        "aws-cdk.aws-iam",
        "aws-cdk.core"
    ],
)
