from aws_cdk import (
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_iam as iam,
    core
)


class HalloumiEksCluster(object):
    '''
    EKS Cluster, with nodegroups.
    '''
    def parse_from_config(self, config: dict, variable: str, default=None):
        try:
            value = config[variable]
        except KeyError:
            value = default
        return value

    def __init__(
        self,
        scope: core.Construct,
        config: dict,
        vpc=[],
        **kwargs
    ) -> None:

        _stack_name = scope.node.id

        self.eks_cluster_public_subnet_name = (
            self.parse_from_config(
                config,
                'eks_cluster_public_subnet_name',
                'eks_public'
            )
        )
        self.eks_cluster_private_subnet_name = (
            self.parse_from_config(
                config,
                'eks_cluster_private_subnet_name',
                'eks_private'
            )
        )
        self.eks_cluster_name = (
            self.parse_from_config(
                config,
                'eks_cluster_name',
                'EksCluster'
            )
        )
        self.eks_version = (
            self.parse_from_config(
                config,
                'kubernetes_version',
                '1.14'
            )
        )
        self.nodegroups = (
            self.parse_from_config(
                config,
                'nodegroups',
                {
                    'DefaultNodegroup': {
                        'instance_types': [
                            't3.small'
                        ]
                    }
                }
            )
        )

        if not vpc:
            # prerequisites for EKS
            self.vpc = ec2.Vpc(
                scope, 'Vpc',
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
        else:
            if len(vpc) > 1:
                raise ValueError('vpc[] currently supports only one item')
            if not isinstance(vpc[0], ec2.IVpc):
                raise ValueError(
                    'vpc should be of type [aws_cdk.aws_ec2.IVpc]'
                )
            self.vpc = vpc[0]

        # Cluster security group
        self.control_plane_security_group = ec2.SecurityGroup(
            scope, f'{_stack_name}ControlPlaneSecurityGroup',
            description=(
                f'EKS Cluster security group for stack: {scope.stack_name}'
            ),
            vpc=self.vpc
        )

        # EKS Cluster IAM Role
        self.cluster_role = iam.Role(
            scope, f'{_stack_name}ClusterServiceRole',
            assumed_by=iam.ServicePrincipal('eks.amazonaws.com'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    'AmazonEKSClusterPolicy'
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    'AmazonEKSServicePolicy'
                )
            ]
        )

        # EKS Cluster
        __public_sids = self.vpc.select_subnets(
            subnet_name=self.eks_cluster_public_subnet_name
        ).subnet_ids

        __private_sids = self.vpc.select_subnets(
            subnet_name=self.eks_cluster_private_subnet_name
        ).subnet_ids

        self.cluster = eks.CfnCluster(
            scope, f'{_stack_name}Cluster',
            name=self.eks_cluster_name,
            resources_vpc_config={
                'securityGroupIds': [
                    self.control_plane_security_group.security_group_name
                ],
                'subnetIds': __public_sids + __private_sids
            },
            role_arn=self.cluster_role.role_arn,
            version=self.eks_version
        )

        # EKS Nodegroup IAM Role
        nodegroup_role = iam.Role(
            scope, f'{_stack_name}NodegroupServiceRole',
            assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    'AmazonEKSWorkerNodePolicy'
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    'AmazonEKS_CNI_Policy'
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    'AmazonEC2ContainerRegistryReadOnly'
                )
            ]
        )

        # EKS Nodegroup
        nodegroups = {}
        for nodegroup in self.nodegroups:
            release_version = None
            try:
                release_version = self.nodegroups[nodegroup]['release_version']
            except KeyError:
                pass

            remote_access = None
            try:
                remote_access = self.nodegroups[nodegroup]['remote_access']
            except KeyError:
                pass

            nodegroups[nodegroup] = eks.CfnNodegroup(
                scope, f'{_stack_name}{nodegroup}',
                cluster_name=self.cluster.name,
                instance_types=self.nodegroups[nodegroup]['instance_types'],
                node_role=nodegroup_role.role_arn,
                release_version=release_version,
                remote_access=remote_access,
                subnets=self.vpc.select_subnets(
                    subnet_name=self.eks_cluster_private_subnet_name
                ).subnet_ids
            )
            nodegroups[nodegroup].add_depends_on(self.cluster)
