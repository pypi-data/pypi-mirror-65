from aws_cdk import (
    aws_cloudformation as cfn,
    aws_ec2 as ec2,
    core
)


class SampleAppStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

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