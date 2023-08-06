from aws_cdk import (
    aws_cloudformation as cfn,
    aws_ec2 as ec2,
    core
)


class SampleAppStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)