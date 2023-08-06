[![Github](https://img.shields.io/badge/github-sentiampc%2Fhcdk--eks-blue.svg)](https://github.com/sentiampc/hcdk-eks)


# Halloumi EKS for the CDK

EKS library for the Halloumi modules of the AWS CDK

## Installation

`pip install hcdk_eks`

## Usage

Halloumi EKS can be used as a basis to deploy EKS clusters with managed Nodegroups on AWS using the CDK.

### Passing your own VPC

**Example**

Within a sample stack, the following example code should be present for minimum functionality.

```python
self.eks_cluster_public_subnet_name = 'eks_public'
self.eks_cluster_private_subnet_name = 'eks_private'
self.eks_cluster_name = 'EksCluster'
self.eks_stack_name = 'eks-cluster-stack'

# prerequisites for EKS
self.vpc = ec2.Vpc(
    self, 'Vpc',
    cidr='10.0.0.0/16',
    max_azs=99,  # use all available AZs,
    subnet_configuration=[
        {
            'cidrMask': 26,
            'name': self.eks_cluster_public_subnet_name,
            'subnetType': ec2.SubnetType.PUBLIC
        },
        {
            'cidrMask': 24,
            'name': self.eks_cluster_private_subnet_name,
            'subnetType': ec2.SubnetType.PRIVATE
        }
    ]
)

# Add necessary tags to subnets for the EKS Cluster
private_eks_subnets = self.vpc.select_subnets(
    subnet_name=self.eks_cluster_private_subnet_name
).subnets
for subnet in private_eks_subnets:
    core.Tag.add(
        subnet,
        key=f'kubernetes.io/cluster/{self.eks_cluster_name}',
        value='shared'
    )
    core.Tag.add(
        subnet,
        key=f'kubernetes.io/role/internal-elb',
        value='1'
    )

# Add necessary tags to subnets for the EKS Cluster
public_eks_subnets = self.vpc.select_subnets(
    subnet_name=self.eks_cluster_public_subnet_name
).subnets
for subnet in public_eks_subnets:
    core.Tag.add(
        subnet,
        key=f'kubernetes.io/cluster/{self.eks_cluster_name}',
        value='shared'
    )
    core.Tag.add(
        subnet,
        key=f'kubernetes.io/role/elb',
        value='1'
    )
```

### EKS Cluster

**Example**

```python
from hcdk_eks import HalloumiEksCluster

app = core.App()

sample_stack = SampleAppStack(app, "sample-app")

__config_eks_cluster = {
    'stack_name': sample_stack.eks_stack_name,
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

eks_stack = cfn.NestedStack(
    sample_stack, 'eks-stack'
)

HalloumiEksCluster(
    scope=eks_stack,
    vpc=sample_stack.vpc,
    config=__config_eks_cluster
)

app.synth()
```

### Using the VPC from the module

**Example**

```python
from hcdk_eks import HalloumiEksCluster

app = core.App()
sample_stack = SampleAppStack(app, "sample-app")

__config_eks_cluster = {
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
    config=__config_eks_cluster
)

synth = app.synth()
```