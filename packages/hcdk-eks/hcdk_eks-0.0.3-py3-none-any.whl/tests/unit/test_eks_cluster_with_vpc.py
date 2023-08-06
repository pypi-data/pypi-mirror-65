import os
import pytest
import json

from aws_cdk import (
    aws_cloudformation as cfn,
    aws_ec2 as ec2,
    core
)
import aws_cdk
from tests.sample_stack_with_vpc import SampleAppStack
from hcdk_eks import HalloumiEksCluster

class TestHalloumiEksCluster:

    def get_template(self):
        app = core.App()
        sample_stack = SampleAppStack(app, "sample-app")

        # Configuration for EKS Cluster Stack

        __config_eks_cluster = {
            'eks_cluster_public_subnet_name': sample_stack.eks_cluster_public_subnet_name,
            'eks_cluster_private_subnet_name': sample_stack.eks_cluster_private_subnet_name,
            'eks_cluster_name': sample_stack.eks_cluster_name,
            'kubernetes_version': '1.14',
            'nodegroups': {
                'nodegroup1': {
                    'instance_types': [
                        't3.large'
                    ]
                },
                'nodegroup2': {
                    'instance_types': [
                        't3.xlarge'
                    ]
                }
            }
        }

        # EKS Cluster Stack
        eks_cluster_stack = cfn.NestedStack(
            sample_stack, 'eks-cluster-stack'
        )

        eks_cluster = HalloumiEksCluster(
            scope=eks_cluster_stack,
            config=__config_eks_cluster,
            vpc=[sample_stack.vpc]
        )

        synth = app.synth()
        with open(
                os.path.join(
                    synth.directory,
                    eks_cluster_stack.template_file
                )
            ) as template:
            return template.read()

    def organize_template(cls, template):
        template = json.loads(template)
        objects = {}
        for key, resource in template['Resources'].items():
            obj_type = resource['Type']
            resource['Id'] = key
            if not objects.get(obj_type):
                objects[obj_type] = []
            objects[obj_type].append(resource)
        return objects

    @classmethod
    def setup_class(cls):
        cls.template = cls.get_template(cls)
        cls.resources = cls.organize_template(cls, cls.template)

    def test_resources(self):
        assert 1 == len(self.resources['AWS::EKS::Cluster'])
        assert 2 == len(self.resources['AWS::EKS::Nodegroup'])
        assert 2 == len(self.resources['AWS::IAM::Role'])

    def test_cluster(self):
        cluster = self.resources['AWS::EKS::Cluster'][0]
        assert cluster['Id'] == 'eksclusterstackCluster'
        assert cluster['Properties']['Version'] == '1.14'

    def test_nodegroups(self):
        for idx, ng in enumerate(self.resources['AWS::EKS::Nodegroup']):
            if idx == 0:
                assert ng['Id'] == 'eksclusterstacknodegroup1'
                assert ng['Properties']['InstanceTypes'] == ['t3.large']
            elif idx == 1:
                assert ng['Id'] == 'eksclusterstacknodegroup2'
                assert ng['Properties']['InstanceTypes'] == ['t3.xlarge']