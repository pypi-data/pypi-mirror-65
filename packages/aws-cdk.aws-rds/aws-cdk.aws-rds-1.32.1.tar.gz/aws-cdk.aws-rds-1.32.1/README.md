## Amazon Relational Database Service Construct Library

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

### Starting a Clustered Database

To set up a clustered database (like Aurora), define a `DatabaseCluster`. You must
always launch a database in a VPC. Use the `vpcSubnets` attribute to control whether
your instances will be launched privately or publicly:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster = DatabaseCluster(self, "Database",
    engine=DatabaseClusterEngine.AURORA,
    master_user={
        "username": "admin"
    },
    instance_props={
        "instance_type": ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
        "vpc_subnets": {
            "subnet_type": ec2.SubnetType.PUBLIC
        },
        "vpc": vpc
    }
)
```

By default, the master password will be generated and stored in AWS Secrets Manager with auto-generated description.

Your cluster will be empty by default. To add a default database upon construction, specify the
`defaultDatabaseName` attribute.

### Starting an Instance Database

To set up a instance database, define a `DatabaseInstance`. You must
always launch a database in a VPC. Use the `vpcSubnets` attribute to control whether
your instances will be launched privately or publicly:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
instance = DatabaseInstance(stack, "Instance",
    engine=rds.DatabaseInstanceEngine.ORACLE_SE1,
    instance_class=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
    master_username="syscdk",
    vpc=vpc
)
```

By default, the master password will be generated and stored in AWS Secrets Manager.

To use the storage auto scaling option of RDS you can specify the maximum allocated storage.
This is the upper limit to which RDS can automatically scale the storage. More info can be found
[here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIOPS.StorageTypes.html#USER_PIOPS.Autoscaling)
Example for max storage configuration:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
instance = DatabaseInstance(stack, "Instance",
    engine=rds.DatabaseInstanceEngine.ORACLE_SE1,
    instance_class=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
    master_username="syscdk",
    vpc=vpc,
    max_allocated_storage=200
)
```

Use `DatabaseInstanceFromSnapshot` and `DatabaseInstanceReadReplica` to create an instance from snapshot or
a source database respectively:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
DatabaseInstanceFromSnapshot(stack, "Instance",
    snapshot_identifier="my-snapshot",
    engine=rds.DatabaseInstanceEngine.POSTGRES,
    instance_class=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.LARGE),
    vpc=vpc
)

DatabaseInstanceReadReplica(stack, "ReadReplica",
    source_database_instance=source_instance,
    engine=rds.DatabaseInstanceEngine.POSTGRES,
    instance_class=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.LARGE),
    vpc=vpc
)
```

Creating a "production" Oracle database instance with option and parameter groups:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Set open cursors with parameter group
parameter_group = rds.ParameterGroup(self, "ParameterGroup",
    family="oracle-se1-11.2",
    parameters={
        "open_cursors": "2500"
    }
)

option_group = rds.OptionGroup(self, "OptionGroup",
    engine=rds.DatabaseInstanceEngine.ORACLE_SE1,
    major_engine_version="11.2",
    configurations=[OptionConfiguration(
        name="XMLDB"
    ), OptionConfiguration(
        name="OEM",
        port=1158,
        vpc=vpc
    )
    ]
)

# Allow connections to OEM
option_group.option_connections.OEM.connections.allow_default_port_from_any_ipv4()

# Database instance with production values
instance = rds.DatabaseInstance(self, "Instance",
    engine=rds.DatabaseInstanceEngine.ORACLE_SE1,
    license_model=rds.LicenseModel.BRING_YOUR_OWN_LICENSE,
    instance_class=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM),
    multi_az=True,
    storage_type=rds.StorageType.IO1,
    master_username="syscdk",
    vpc=vpc,
    database_name="ORCL",
    storage_encrypted=True,
    backup_retention=cdk.Duration.days(7),
    monitoring_interval=cdk.Duration.seconds(60),
    enable_performance_insights=True,
    cloudwatch_logs_exports=["trace", "audit", "alert", "listener"
    ],
    cloudwatch_logs_retention=logs.RetentionDays.ONE_MONTH,
    auto_minor_version_upgrade=False,
    option_group=option_group,
    parameter_group=parameter_group
)

# Allow connections on default port from any IPV4
instance.connections.allow_default_port_from_any_ipv4()

# Rotate the master user password every 30 days
instance.add_rotation_single_user()

# Add alarm for high CPU
cloudwatch.Alarm(self, "HighCPU",
    metric=instance.metric_cPUUtilization(),
    threshold=90,
    evaluation_periods=1
)

# Trigger Lambda function on instance availability events
fn = lambda.Function(self, "Function",
    code=lambda.Code.from_inline("exports.handler = (event) => console.log(event);"),
    handler="index.handler",
    runtime=lambda.Runtime.NODEJS_10_X
)

availability_rule = instance.on_event("Availability", target=targets.LambdaFunction(fn))
availability_rule.add_event_pattern(
    detail={
        "EventCategories": ["availability"
        ]
    }
)
```

Add XMLDB and OEM with option group

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# Set open cursors with parameter group
parameter_group = rds.ParameterGroup(self, "ParameterGroup",
    family="oracle-se1-11.2",
    parameters={
        "open_cursors": "2500"
    }
)

option_group = rds.OptionGroup(self, "OptionGroup",
    engine=rds.DatabaseInstanceEngine.ORACLE_SE1,
    major_engine_version="11.2",
    configurations=[OptionConfiguration(
        name="XMLDB"
    ), OptionConfiguration(
        name="OEM",
        port=1158,
        vpc=vpc
    )
    ]
)

# Allow connections to OEM
option_group.option_connections.OEM.connections.allow_default_port_from_any_ipv4()

# Database instance with production values
instance = rds.DatabaseInstance(self, "Instance",
    engine=rds.DatabaseInstanceEngine.ORACLE_SE1,
    license_model=rds.LicenseModel.BRING_YOUR_OWN_LICENSE,
    instance_class=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM),
    multi_az=True,
    storage_type=rds.StorageType.IO1,
    master_username="syscdk",
    vpc=vpc,
    database_name="ORCL",
    storage_encrypted=True,
    backup_retention=cdk.Duration.days(7),
    monitoring_interval=cdk.Duration.seconds(60),
    enable_performance_insights=True,
    cloudwatch_logs_exports=["trace", "audit", "alert", "listener"
    ],
    cloudwatch_logs_retention=logs.RetentionDays.ONE_MONTH,
    auto_minor_version_upgrade=False,
    option_group=option_group,
    parameter_group=parameter_group
)

# Allow connections on default port from any IPV4
instance.connections.allow_default_port_from_any_ipv4()

# Rotate the master user password every 30 days
instance.add_rotation_single_user()

# Add alarm for high CPU
cloudwatch.Alarm(self, "HighCPU",
    metric=instance.metric_cPUUtilization(),
    threshold=90,
    evaluation_periods=1
)

# Trigger Lambda function on instance availability events
fn = lambda.Function(self, "Function",
    code=lambda.Code.from_inline("exports.handler = (event) => console.log(event);"),
    handler="index.handler",
    runtime=lambda.Runtime.NODEJS_10_X
)

availability_rule = instance.on_event("Availability", target=targets.LambdaFunction(fn))
availability_rule.add_event_pattern(
    detail={
        "EventCategories": ["availability"
        ]
    }
)
```

### Instance events

To define Amazon CloudWatch event rules for database instances, use the `onEvent`
method:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
rule = instance.on_event("InstanceEvent", target=targets.LambdaFunction(fn))
```

### Connecting

To control who can access the cluster or instance, use the `.connections` attribute. RDS databases have
a default port, so you don't need to specify the port:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.connections.allow_from_any_ipv4("Open to the world")
```

The endpoints to access your database cluster will be available as the `.clusterEndpoint` and `.readerEndpoint`
attributes:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
write_address = cluster.cluster_endpoint.socket_address
```

For an instance database:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
address = instance.instance_endpoint.socket_address
```

### Rotating credentials

When the master password is generated and stored in AWS Secrets Manager, it can be rotated automatically:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
instance.add_rotation_single_user()
```

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cluster = rds.DatabaseCluster(stack, "Database",
    engine=rds.DatabaseClusterEngine.AURORA,
    master_user=Login(
        username="admin"
    ),
    instance_props={
        "instance_type": ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.SMALL),
        "vpc": vpc
    }
)

cluster.add_rotation_single_user()
```

The multi user rotation scheme is also available:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
instance.add_rotation_multi_user("MyUser",
    secret=my_imported_secret
)
```

It's also possible to create user credentials together with the instance/cluster and add rotation:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_user_secret = rds.DatabaseSecret(self, "MyUserSecret",
    username="myuser",
    master_secret=instance.secret
)
my_user_secret_attached = my_user_secret.attach(instance)# Adds DB connections information in the secret

instance.add_rotation_multi_user("MyUser", # Add rotation using the multi user scheme
    secret=my_user_secret_attached)
```

**Note**: This user must be created manually in the database using the master credentials.
The rotation will start as soon as this user exists.

See also [@aws-cdk/aws-secretsmanager](https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-secretsmanager/README.md) for credentials rotation of existing clusters/instances.

### Metrics

Database instances expose metrics (`cloudwatch.Metric`):

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# The number of database connections in use (average over 5 minutes)
db_connections = instance.metric_database_connections()

# The average amount of time taken per disk I/O operation (average over 1 minute)
read_latency = instance.metric("ReadLatency", statistic="Average", period_sec=60)
```

### Enabling S3 integration to a cluster (non-serverless Aurora only)

Data in S3 buckets can be imported to and exported from Aurora databases using SQL queries. To enable this
functionality, set the `s3ImportBuckets` and `s3ExportBuckets` properties for import and export respectively. When
configured, the CDK automatically creates and configures IAM roles as required.
Additionally, the `s3ImportRole` and `s3ExportRole` properties can be used to set this role directly.

For Aurora MySQL, read more about [loading data from
S3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Integrating.LoadFromS3.html) and [saving
data into S3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Integrating.SaveIntoS3.html).

For Aurora PostgreSQL, read more about [loading data from
S3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Migrating.html) and [saving
data into S3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/postgresql-s3-export.html).

The following snippet sets up a database cluster with different S3 buckets where the data is imported and exported -

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import_bucket = s3.Bucket(self, "importbucket")
export_bucket = s3.Bucket(self, "exportbucket")
DatabaseCluster(self, "dbcluster",
    # ...
    s3_import_buckets=[import_bucket],
    s3_export_buckets=[export_bucket]
)
```
