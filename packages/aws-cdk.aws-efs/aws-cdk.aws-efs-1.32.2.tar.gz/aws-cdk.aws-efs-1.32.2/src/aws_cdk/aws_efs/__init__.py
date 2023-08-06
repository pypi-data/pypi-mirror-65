"""
## Amazon Elastic File System Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module.**
>
> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib))
> are auto-generated from CloudFormation. They are stable and safe to use.
>
> However, all other classes, i.e., higher level constructs, are under active development and subject to non-backward
> compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This construct library allows you to set up AWS Elastic File System (EFS).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_efs as efs

my_vpc = ec2.Vpc(self, "VPC")
file_system = efs.EfsFileSystem(self, "MyEfsFileSystem",
    vpc=my_vpc,
    encrypted=True,
    lifecycle_policy=EfsLifecyclePolicyProperty.AFTER_14_DAYS,
    performance_mode=EfsPerformanceMode.GENERAL_PURPOSE,
    throughput_mode=EfsThroughputMode.BURSTING
)
```

### Connecting

To control who can access the EFS, use the `.connections` attribute. EFS has
a fixed default port, so you don't need to specify the port:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
file_system.connections.allow_default_port_from(instance)
```

### Mounting the file system using User Data

In order to automatically mount this file system during instance launch,
following code can be used as reference:

```
const vpc = new ec2.Vpc(this, 'VPC');

const fileSystem = new efs.EfsFileSystem(this, 'EfsFileSystem', {
  vpc,
  encrypted: true,
  lifecyclePolicy: efs.EfsLifecyclePolicyProperty.AFTER_14_DAYS,
  performanceMode: efs.EfsPerformanceMode.GENERAL_PURPOSE,
  throughputMode: efs.EfsThroughputMode.BURSTING
});

const inst = new Instance(this, 'inst', {
  instanceType: InstanceType.of(InstanceClass.T2, InstanceSize.LARGE),
  machineImage: new AmazonLinuxImage({
    generation: AmazonLinuxGeneration.AMAZON_LINUX_2
  }),
  vpc,
  vpcSubnets: {
    subnetType: SubnetType.PUBLIC,
  }
});

fileSystem.connections.allowDefaultPortFrom(inst);

inst.userData.addCommands("yum check-update -y",    // Ubuntu: apt-get -y update
  "yum upgrade -y",                                 // Ubuntu: apt-get -y upgrade
  "yum install -y amazon-efs-utils",                // Ubuntu: apt-get -y install amazon-efs-utils
  "yum install -y nfs-utils",                       // Ubuntu: apt-get -y install nfs-common
  "file_system_id_1=" + fileSystem.fileSystemId,
  "efs_mount_point_1=/mnt/efs/fs1",
  "mkdir -p \"${efs_mount_point_1}\"",
  "test -f \"/sbin/mount.efs\" && echo \"${file_system_id_1}:/ ${efs_mount_point_1} efs defaults,_netdev\" >> /etc/fstab || " +
  "echo \"${file_system_id_1}.efs." + cdk.Stack.of(this).region + ".amazonaws.com:/ ${efs_mount_point_1} nfs4 nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport,_netdev 0 0\" >> /etc/fstab",
  "mount -a -t efs,nfs4 defaults");
```

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_ec2
import aws_cdk.aws_kms
import aws_cdk.core
import aws_cdk.cx_api
import constructs

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-efs", "1.32.2", __name__, "aws-efs@1.32.2.jsii.tgz")


@jsii.implements(aws_cdk.core.IInspectable)
class CfnFileSystem(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-efs.CfnFileSystem"):
    """A CloudFormation ``AWS::EFS::FileSystem``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html
    cloudformationResource:
    :cloudformationResource:: AWS::EFS::FileSystem
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, encrypted: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, file_system_tags: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ElasticFileSystemTagProperty"]]]]]=None, kms_key_id: typing.Optional[str]=None, lifecycle_policies: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "LifecyclePolicyProperty"]]]]]=None, performance_mode: typing.Optional[str]=None, provisioned_throughput_in_mibps: typing.Optional[jsii.Number]=None, throughput_mode: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EFS::FileSystem``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param encrypted: ``AWS::EFS::FileSystem.Encrypted``.
        :param file_system_tags: ``AWS::EFS::FileSystem.FileSystemTags``.
        :param kms_key_id: ``AWS::EFS::FileSystem.KmsKeyId``.
        :param lifecycle_policies: ``AWS::EFS::FileSystem.LifecyclePolicies``.
        :param performance_mode: ``AWS::EFS::FileSystem.PerformanceMode``.
        :param provisioned_throughput_in_mibps: ``AWS::EFS::FileSystem.ProvisionedThroughputInMibps``.
        :param throughput_mode: ``AWS::EFS::FileSystem.ThroughputMode``.
        """
        props = CfnFileSystemProps(encrypted=encrypted, file_system_tags=file_system_tags, kms_key_id=kms_key_id, lifecycle_policies=lifecycle_policies, performance_mode=performance_mode, provisioned_throughput_in_mibps=provisioned_throughput_in_mibps, throughput_mode=throughput_mode)

        jsii.create(CfnFileSystem, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="encrypted")
    def encrypted(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::EFS::FileSystem.Encrypted``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-encrypted
        """
        return jsii.get(self, "encrypted")

    @encrypted.setter
    def encrypted(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        jsii.set(self, "encrypted", value)

    @builtins.property
    @jsii.member(jsii_name="fileSystemTags")
    def file_system_tags(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ElasticFileSystemTagProperty"]]]]]:
        """``AWS::EFS::FileSystem.FileSystemTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-filesystemtags
        """
        return jsii.get(self, "fileSystemTags")

    @file_system_tags.setter
    def file_system_tags(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ElasticFileSystemTagProperty"]]]]]):
        jsii.set(self, "fileSystemTags", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::EFS::FileSystem.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[str]):
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="lifecyclePolicies")
    def lifecycle_policies(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "LifecyclePolicyProperty"]]]]]:
        """``AWS::EFS::FileSystem.LifecyclePolicies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-elasticfilesystem-filesystem-lifecyclepolicies
        """
        return jsii.get(self, "lifecyclePolicies")

    @lifecycle_policies.setter
    def lifecycle_policies(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "LifecyclePolicyProperty"]]]]]):
        jsii.set(self, "lifecyclePolicies", value)

    @builtins.property
    @jsii.member(jsii_name="performanceMode")
    def performance_mode(self) -> typing.Optional[str]:
        """``AWS::EFS::FileSystem.PerformanceMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-performancemode
        """
        return jsii.get(self, "performanceMode")

    @performance_mode.setter
    def performance_mode(self, value: typing.Optional[str]):
        jsii.set(self, "performanceMode", value)

    @builtins.property
    @jsii.member(jsii_name="provisionedThroughputInMibps")
    def provisioned_throughput_in_mibps(self) -> typing.Optional[jsii.Number]:
        """``AWS::EFS::FileSystem.ProvisionedThroughputInMibps``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-elasticfilesystem-filesystem-provisionedthroughputinmibps
        """
        return jsii.get(self, "provisionedThroughputInMibps")

    @provisioned_throughput_in_mibps.setter
    def provisioned_throughput_in_mibps(self, value: typing.Optional[jsii.Number]):
        jsii.set(self, "provisionedThroughputInMibps", value)

    @builtins.property
    @jsii.member(jsii_name="throughputMode")
    def throughput_mode(self) -> typing.Optional[str]:
        """``AWS::EFS::FileSystem.ThroughputMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-elasticfilesystem-filesystem-throughputmode
        """
        return jsii.get(self, "throughputMode")

    @throughput_mode.setter
    def throughput_mode(self, value: typing.Optional[str]):
        jsii.set(self, "throughputMode", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-efs.CfnFileSystem.ElasticFileSystemTagProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class ElasticFileSystemTagProperty():
        def __init__(self, *, key: str, value: str):
            """
            :param key: ``CfnFileSystem.ElasticFileSystemTagProperty.Key``.
            :param value: ``CfnFileSystem.ElasticFileSystemTagProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-filesystemtags.html
            """
            self._values = {
                'key': key,
                'value': value,
            }

        @builtins.property
        def key(self) -> str:
            """``CfnFileSystem.ElasticFileSystemTagProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-filesystemtags.html#cfn-efs-filesystem-filesystemtags-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> str:
            """``CfnFileSystem.ElasticFileSystemTagProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-filesystemtags.html#cfn-efs-filesystem-filesystemtags-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ElasticFileSystemTagProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-efs.CfnFileSystem.LifecyclePolicyProperty", jsii_struct_bases=[], name_mapping={'transition_to_ia': 'transitionToIa'})
    class LifecyclePolicyProperty():
        def __init__(self, *, transition_to_ia: str):
            """
            :param transition_to_ia: ``CfnFileSystem.LifecyclePolicyProperty.TransitionToIA``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticfilesystem-filesystem-lifecyclepolicy.html
            """
            self._values = {
                'transition_to_ia': transition_to_ia,
            }

        @builtins.property
        def transition_to_ia(self) -> str:
            """``CfnFileSystem.LifecyclePolicyProperty.TransitionToIA``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticfilesystem-filesystem-lifecyclepolicy.html#cfn-elasticfilesystem-filesystem-lifecyclepolicy-transitiontoia
            """
            return self._values.get('transition_to_ia')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LifecyclePolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-efs.CfnFileSystemProps", jsii_struct_bases=[], name_mapping={'encrypted': 'encrypted', 'file_system_tags': 'fileSystemTags', 'kms_key_id': 'kmsKeyId', 'lifecycle_policies': 'lifecyclePolicies', 'performance_mode': 'performanceMode', 'provisioned_throughput_in_mibps': 'provisionedThroughputInMibps', 'throughput_mode': 'throughputMode'})
class CfnFileSystemProps():
    def __init__(self, *, encrypted: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, file_system_tags: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnFileSystem.ElasticFileSystemTagProperty"]]]]]=None, kms_key_id: typing.Optional[str]=None, lifecycle_policies: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnFileSystem.LifecyclePolicyProperty"]]]]]=None, performance_mode: typing.Optional[str]=None, provisioned_throughput_in_mibps: typing.Optional[jsii.Number]=None, throughput_mode: typing.Optional[str]=None):
        """Properties for defining a ``AWS::EFS::FileSystem``.

        :param encrypted: ``AWS::EFS::FileSystem.Encrypted``.
        :param file_system_tags: ``AWS::EFS::FileSystem.FileSystemTags``.
        :param kms_key_id: ``AWS::EFS::FileSystem.KmsKeyId``.
        :param lifecycle_policies: ``AWS::EFS::FileSystem.LifecyclePolicies``.
        :param performance_mode: ``AWS::EFS::FileSystem.PerformanceMode``.
        :param provisioned_throughput_in_mibps: ``AWS::EFS::FileSystem.ProvisionedThroughputInMibps``.
        :param throughput_mode: ``AWS::EFS::FileSystem.ThroughputMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html
        """
        self._values = {
        }
        if encrypted is not None: self._values["encrypted"] = encrypted
        if file_system_tags is not None: self._values["file_system_tags"] = file_system_tags
        if kms_key_id is not None: self._values["kms_key_id"] = kms_key_id
        if lifecycle_policies is not None: self._values["lifecycle_policies"] = lifecycle_policies
        if performance_mode is not None: self._values["performance_mode"] = performance_mode
        if provisioned_throughput_in_mibps is not None: self._values["provisioned_throughput_in_mibps"] = provisioned_throughput_in_mibps
        if throughput_mode is not None: self._values["throughput_mode"] = throughput_mode

    @builtins.property
    def encrypted(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::EFS::FileSystem.Encrypted``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-encrypted
        """
        return self._values.get('encrypted')

    @builtins.property
    def file_system_tags(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnFileSystem.ElasticFileSystemTagProperty"]]]]]:
        """``AWS::EFS::FileSystem.FileSystemTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-filesystemtags
        """
        return self._values.get('file_system_tags')

    @builtins.property
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::EFS::FileSystem.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-kmskeyid
        """
        return self._values.get('kms_key_id')

    @builtins.property
    def lifecycle_policies(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnFileSystem.LifecyclePolicyProperty"]]]]]:
        """``AWS::EFS::FileSystem.LifecyclePolicies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-elasticfilesystem-filesystem-lifecyclepolicies
        """
        return self._values.get('lifecycle_policies')

    @builtins.property
    def performance_mode(self) -> typing.Optional[str]:
        """``AWS::EFS::FileSystem.PerformanceMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-performancemode
        """
        return self._values.get('performance_mode')

    @builtins.property
    def provisioned_throughput_in_mibps(self) -> typing.Optional[jsii.Number]:
        """``AWS::EFS::FileSystem.ProvisionedThroughputInMibps``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-elasticfilesystem-filesystem-provisionedthroughputinmibps
        """
        return self._values.get('provisioned_throughput_in_mibps')

    @builtins.property
    def throughput_mode(self) -> typing.Optional[str]:
        """``AWS::EFS::FileSystem.ThroughputMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-elasticfilesystem-filesystem-throughputmode
        """
        return self._values.get('throughput_mode')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnFileSystemProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnMountTarget(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-efs.CfnMountTarget"):
    """A CloudFormation ``AWS::EFS::MountTarget``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html
    cloudformationResource:
    :cloudformationResource:: AWS::EFS::MountTarget
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, file_system_id: str, security_groups: typing.List[str], subnet_id: str, ip_address: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EFS::MountTarget``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param file_system_id: ``AWS::EFS::MountTarget.FileSystemId``.
        :param security_groups: ``AWS::EFS::MountTarget.SecurityGroups``.
        :param subnet_id: ``AWS::EFS::MountTarget.SubnetId``.
        :param ip_address: ``AWS::EFS::MountTarget.IpAddress``.
        """
        props = CfnMountTargetProps(file_system_id=file_system_id, security_groups=security_groups, subnet_id=subnet_id, ip_address=ip_address)

        jsii.create(CfnMountTarget, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrIpAddress")
    def attr_ip_address(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: IpAddress
        """
        return jsii.get(self, "attrIpAddress")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> str:
        """``AWS::EFS::MountTarget.FileSystemId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-filesystemid
        """
        return jsii.get(self, "fileSystemId")

    @file_system_id.setter
    def file_system_id(self, value: str):
        jsii.set(self, "fileSystemId", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[str]:
        """``AWS::EFS::MountTarget.SecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-securitygroups
        """
        return jsii.get(self, "securityGroups")

    @security_groups.setter
    def security_groups(self, value: typing.List[str]):
        jsii.set(self, "securityGroups", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> str:
        """``AWS::EFS::MountTarget.SubnetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-subnetid
        """
        return jsii.get(self, "subnetId")

    @subnet_id.setter
    def subnet_id(self, value: str):
        jsii.set(self, "subnetId", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> typing.Optional[str]:
        """``AWS::EFS::MountTarget.IpAddress``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-ipaddress
        """
        return jsii.get(self, "ipAddress")

    @ip_address.setter
    def ip_address(self, value: typing.Optional[str]):
        jsii.set(self, "ipAddress", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-efs.CfnMountTargetProps", jsii_struct_bases=[], name_mapping={'file_system_id': 'fileSystemId', 'security_groups': 'securityGroups', 'subnet_id': 'subnetId', 'ip_address': 'ipAddress'})
class CfnMountTargetProps():
    def __init__(self, *, file_system_id: str, security_groups: typing.List[str], subnet_id: str, ip_address: typing.Optional[str]=None):
        """Properties for defining a ``AWS::EFS::MountTarget``.

        :param file_system_id: ``AWS::EFS::MountTarget.FileSystemId``.
        :param security_groups: ``AWS::EFS::MountTarget.SecurityGroups``.
        :param subnet_id: ``AWS::EFS::MountTarget.SubnetId``.
        :param ip_address: ``AWS::EFS::MountTarget.IpAddress``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html
        """
        self._values = {
            'file_system_id': file_system_id,
            'security_groups': security_groups,
            'subnet_id': subnet_id,
        }
        if ip_address is not None: self._values["ip_address"] = ip_address

    @builtins.property
    def file_system_id(self) -> str:
        """``AWS::EFS::MountTarget.FileSystemId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-filesystemid
        """
        return self._values.get('file_system_id')

    @builtins.property
    def security_groups(self) -> typing.List[str]:
        """``AWS::EFS::MountTarget.SecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-securitygroups
        """
        return self._values.get('security_groups')

    @builtins.property
    def subnet_id(self) -> str:
        """``AWS::EFS::MountTarget.SubnetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-subnetid
        """
        return self._values.get('subnet_id')

    @builtins.property
    def ip_address(self) -> typing.Optional[str]:
        """``AWS::EFS::MountTarget.IpAddress``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-ipaddress
        """
        return self._values.get('ip_address')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnMountTargetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-efs.EfsFileSystemAttributes", jsii_struct_bases=[], name_mapping={'file_system_id': 'fileSystemID', 'security_group': 'securityGroup'})
class EfsFileSystemAttributes():
    def __init__(self, *, file_system_id: str, security_group: aws_cdk.aws_ec2.ISecurityGroup):
        """Properties that describe an existing EFS file system.

        :param file_system_id: The File System's ID.
        :param security_group: The security group of the file system.

        stability
        :stability: experimental
        """
        self._values = {
            'file_system_id': file_system_id,
            'security_group': security_group,
        }

    @builtins.property
    def file_system_id(self) -> str:
        """The File System's ID.

        stability
        :stability: experimental
        """
        return self._values.get('file_system_id')

    @builtins.property
    def security_group(self) -> aws_cdk.aws_ec2.ISecurityGroup:
        """The security group of the file system.

        stability
        :stability: experimental
        """
        return self._values.get('security_group')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EfsFileSystemAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-efs.EfsFileSystemProps", jsii_struct_bases=[], name_mapping={'vpc': 'vpc', 'encrypted': 'encrypted', 'kms_key': 'kmsKey', 'lifecycle_policy': 'lifecyclePolicy', 'performance_mode': 'performanceMode', 'provisioned_throughput_in_mibps': 'provisionedThroughputInMibps', 'security_group': 'securityGroup', 'throughput_mode': 'throughputMode', 'vpc_subnets': 'vpcSubnets'})
class EfsFileSystemProps():
    def __init__(self, *, vpc: aws_cdk.aws_ec2.IVpc, encrypted: typing.Optional[bool]=None, kms_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, lifecycle_policy: typing.Optional["EfsLifecyclePolicyProperty"]=None, performance_mode: typing.Optional["EfsPerformanceMode"]=None, provisioned_throughput_in_mibps: typing.Optional[jsii.Number]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, throughput_mode: typing.Optional["EfsThroughputMode"]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None):
        """Properties of EFS FileSystem.

        :param vpc: VPC to launch the file system in.
        :param encrypted: Defines if the data at rest in the file system is encrypted or not. Default: - false
        :param kms_key: The KMS key used for encryption. This is required to encrypt the data at rest if @encrypted is set to true. Default: - if
        :param lifecycle_policy: A policy used by EFS lifecycle management to transition files to the Infrequent Access (IA) storage class. Default: - none
        :param performance_mode: Enum to mention the performance mode of the file system. Default: - GENERAL_PURPOSE
        :param provisioned_throughput_in_mibps: Provisioned throughput for the file system. This is a required property if the throughput mode is set to PROVISIONED. Valid values are 1-1024. Default: - None, errors out
        :param security_group: Security Group to assign to this file system. Default: - creates new security group which allow all out bound traffic
        :param throughput_mode: Enum to mention the throughput mode of the file system. Default: - BURSTING
        :param vpc_subnets: Where to place the mount target within the VPC. Default: - Private subnets

        stability
        :stability: experimental
        """
        if isinstance(vpc_subnets, dict): vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values = {
            'vpc': vpc,
        }
        if encrypted is not None: self._values["encrypted"] = encrypted
        if kms_key is not None: self._values["kms_key"] = kms_key
        if lifecycle_policy is not None: self._values["lifecycle_policy"] = lifecycle_policy
        if performance_mode is not None: self._values["performance_mode"] = performance_mode
        if provisioned_throughput_in_mibps is not None: self._values["provisioned_throughput_in_mibps"] = provisioned_throughput_in_mibps
        if security_group is not None: self._values["security_group"] = security_group
        if throughput_mode is not None: self._values["throughput_mode"] = throughput_mode
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """VPC to launch the file system in.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def encrypted(self) -> typing.Optional[bool]:
        """Defines if the data at rest in the file system is encrypted or not.

        default
        :default: - false

        stability
        :stability: experimental
        """
        return self._values.get('encrypted')

    @builtins.property
    def kms_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The KMS key used for encryption.

        This is required to encrypt the data at rest if @encrypted is set to true.

        default
        :default: - if

        stability
        :stability: experimental
        encrypted:
        :encrypted:: is true, the default key for EFS (/aws/elasticfilesystem) is used
        """
        return self._values.get('kms_key')

    @builtins.property
    def lifecycle_policy(self) -> typing.Optional["EfsLifecyclePolicyProperty"]:
        """A policy used by EFS lifecycle management to transition files to the Infrequent Access (IA) storage class.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('lifecycle_policy')

    @builtins.property
    def performance_mode(self) -> typing.Optional["EfsPerformanceMode"]:
        """Enum to mention the performance mode of the file system.

        default
        :default: - GENERAL_PURPOSE

        stability
        :stability: experimental
        """
        return self._values.get('performance_mode')

    @builtins.property
    def provisioned_throughput_in_mibps(self) -> typing.Optional[jsii.Number]:
        """Provisioned throughput for the file system.

        This is a required property if the throughput mode is set to PROVISIONED.
        Valid values are 1-1024.

        default
        :default: - None, errors out

        stability
        :stability: experimental
        """
        return self._values.get('provisioned_throughput_in_mibps')

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Security Group to assign to this file system.

        default
        :default: - creates new security group which allow all out bound traffic

        stability
        :stability: experimental
        """
        return self._values.get('security_group')

    @builtins.property
    def throughput_mode(self) -> typing.Optional["EfsThroughputMode"]:
        """Enum to mention the throughput mode of the file system.

        default
        :default: - BURSTING

        stability
        :stability: experimental
        """
        return self._values.get('throughput_mode')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place the mount target within the VPC.

        default
        :default: - Private subnets

        stability
        :stability: experimental
        """
        return self._values.get('vpc_subnets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EfsFileSystemProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-efs.EfsLifecyclePolicyProperty")
class EfsLifecyclePolicyProperty(enum.Enum):
    """EFS Lifecycle Policy, if a file is not accessed for given days, it will move to EFS Infrequent Access.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-elasticfilesystem-filesystem-lifecyclepolicies
    stability
    :stability: experimental
    """
    AFTER_7_DAYS = "AFTER_7_DAYS"
    """After 7 days of not being accessed.

    stability
    :stability: experimental
    """
    AFTER_14_DAYS = "AFTER_14_DAYS"
    """After 14 days of not being accessed.

    stability
    :stability: experimental
    """
    AFTER_30_DAYS = "AFTER_30_DAYS"
    """After 30 days of not being accessed.

    stability
    :stability: experimental
    """
    AFTER_60_DAYS = "AFTER_60_DAYS"
    """After 60 days of not being accessed.

    stability
    :stability: experimental
    """
    AFTER_90_DAYS = "AFTER_90_DAYS"
    """After 90 days of not being accessed.

    stability
    :stability: experimental
    """

@jsii.enum(jsii_type="@aws-cdk/aws-efs.EfsPerformanceMode")
class EfsPerformanceMode(enum.Enum):
    """EFS Performance mode.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-performancemode
    stability
    :stability: experimental
    """
    GENERAL_PURPOSE = "GENERAL_PURPOSE"
    """This is the general purpose performance mode for most file systems.

    stability
    :stability: experimental
    """
    MAX_IO = "MAX_IO"
    """This performance mode can scale to higher levels of aggregate throughput and operations per second with a tradeoff of slightly higher latencies.

    stability
    :stability: experimental
    """

@jsii.enum(jsii_type="@aws-cdk/aws-efs.EfsThroughputMode")
class EfsThroughputMode(enum.Enum):
    """EFS Throughput mode.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-elasticfilesystem-filesystem-throughputmode
    stability
    :stability: experimental
    """
    BURSTING = "BURSTING"
    """This mode on Amazon EFS scales as the size of the file system in the standard storage class grows.

    stability
    :stability: experimental
    """
    PROVISIONED = "PROVISIONED"
    """This mode can instantly provision the throughput of the file system (in MiB/s) independent of the amount of data stored.

    stability
    :stability: experimental
    """

@jsii.interface(jsii_type="@aws-cdk/aws-efs.IEfsFileSystem")
class IEfsFileSystem(aws_cdk.aws_ec2.IConnectable, jsii.compat.Protocol):
    """Interface to implement AWS File Systems.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IEfsFileSystemProxy

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> str:
        """The ID of the file system, assigned by Amazon EFS.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IEfsFileSystemProxy(jsii.proxy_for(aws_cdk.aws_ec2.IConnectable)):
    """Interface to implement AWS File Systems.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-efs.IEfsFileSystem"
    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> str:
        """The ID of the file system, assigned by Amazon EFS.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "fileSystemId")


@jsii.implements(IEfsFileSystem)
class EfsFileSystem(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-efs.EfsFileSystem"):
    """The Elastic File System implementation of IFileSystem.

    It creates a new, empty file system in Amazon Elastic File System (Amazon EFS).
    It also creates mount target (AWS::EFS::MountTarget) implicitly to mount the
    EFS file system on an Amazon Elastic Compute Cloud (Amazon EC2) instance or another resource.

    see
    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html
    stability
    :stability: experimental
    resource:
    :resource:: AWS::EFS::FileSystem
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, vpc: aws_cdk.aws_ec2.IVpc, encrypted: typing.Optional[bool]=None, kms_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, lifecycle_policy: typing.Optional["EfsLifecyclePolicyProperty"]=None, performance_mode: typing.Optional["EfsPerformanceMode"]=None, provisioned_throughput_in_mibps: typing.Optional[jsii.Number]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, throughput_mode: typing.Optional["EfsThroughputMode"]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        """Constructor for creating a new EFS FileSystem.

        :param scope: -
        :param id: -
        :param vpc: VPC to launch the file system in.
        :param encrypted: Defines if the data at rest in the file system is encrypted or not. Default: - false
        :param kms_key: The KMS key used for encryption. This is required to encrypt the data at rest if @encrypted is set to true. Default: - if
        :param lifecycle_policy: A policy used by EFS lifecycle management to transition files to the Infrequent Access (IA) storage class. Default: - none
        :param performance_mode: Enum to mention the performance mode of the file system. Default: - GENERAL_PURPOSE
        :param provisioned_throughput_in_mibps: Provisioned throughput for the file system. This is a required property if the throughput mode is set to PROVISIONED. Valid values are 1-1024. Default: - None, errors out
        :param security_group: Security Group to assign to this file system. Default: - creates new security group which allow all out bound traffic
        :param throughput_mode: Enum to mention the throughput mode of the file system. Default: - BURSTING
        :param vpc_subnets: Where to place the mount target within the VPC. Default: - Private subnets

        stability
        :stability: experimental
        """
        props = EfsFileSystemProps(vpc=vpc, encrypted=encrypted, kms_key=kms_key, lifecycle_policy=lifecycle_policy, performance_mode=performance_mode, provisioned_throughput_in_mibps=provisioned_throughput_in_mibps, security_group=security_group, throughput_mode=throughput_mode, vpc_subnets=vpc_subnets)

        jsii.create(EfsFileSystem, self, [scope, id, props])

    @jsii.member(jsii_name="fromEfsFileSystemAttributes")
    @builtins.classmethod
    def from_efs_file_system_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, file_system_id: str, security_group: aws_cdk.aws_ec2.ISecurityGroup) -> "IEfsFileSystem":
        """Import an existing File System from the given properties.

        :param scope: -
        :param id: -
        :param file_system_id: The File System's ID.
        :param security_group: The security group of the file system.

        stability
        :stability: experimental
        """
        attrs = EfsFileSystemAttributes(file_system_id=file_system_id, security_group=security_group)

        return jsii.sinvoke(cls, "fromEfsFileSystemAttributes", [scope, id, attrs])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """The security groups/rules used to allow network connections to the file system.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> str:
        """The ID of the file system, assigned by Amazon EFS.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "fileSystemId")


__all__ = ["CfnFileSystem", "CfnFileSystemProps", "CfnMountTarget", "CfnMountTargetProps", "EfsFileSystem", "EfsFileSystemAttributes", "EfsFileSystemProps", "EfsLifecyclePolicyProperty", "EfsPerformanceMode", "EfsThroughputMode", "IEfsFileSystem", "__jsii_assembly__"]

publication.publish()
