## AWS Cloud9 Construct Library

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

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

AWS Cloud9 is a cloud-based integrated development environment (IDE) that lets you write, run, and debug your code with just a browser. It includes a code editor, debugger, and terminal. Cloud9 comes prepackaged with essential tools for popular programming languages, including JavaScript, Python, PHP, and more, so you don’t need to install files or configure your development machine to start new projects. Since your Cloud9 IDE is cloud-based, you can work on your projects from your office, home, or anywhere using an internet-connected machine. Cloud9 also provides a seamless experience for developing serverless applications enabling you to easily define resources, debug, and switch between local and remote execution of serverless applications. With Cloud9, you can quickly share your development environment with your team, enabling you to pair program and track each other's inputs in real time.

### Creating EC2 Environment

EC2 Environments are defined with `Ec2Environment`. To create an EC2 environment in the private subnet, specify `subnetSelection` with private `subnetType`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_cloud9 as cloud9

# create a cloud9 ec2 environment in a new VPC
vpc = ec2.Vpc(self, "VPC", max_azs=3)
cloud9.Ec2Environment(self, "Cloud9Env", vpc=vpc)

# or create the cloud9 environment in the default VPC with specific instanceType
default_vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)
cloud9.Ec2Environment(self, "Cloud9Env2",
    vpc=default_vpc,
    instance_type=ec2.InstanceType("t3.large")
)

# or specify in a different subnetSelection
c9env = cloud9.Ec2Environment(self, "Cloud9Env3",
    vpc=vpc,
    subnet_selection=SubnetSelection(
        subnet_type=ec2.SubnetType.PRIVATE
    )
)

# print the Cloud9 IDE URL in the output
cdk.CfnOutput(self, "URL", value=c9env.ide_url)
```
