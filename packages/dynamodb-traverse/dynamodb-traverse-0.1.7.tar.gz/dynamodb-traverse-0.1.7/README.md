# dynamodb-traverse
High performance, thread safe, hackable, general purpose traversing tool for AWS DynamoDB based on aioboto3.
<p align="left">
<a href="https://travis-ci/holyshipt/dynamodb_traverse"><img alt="Build Status" src="https://travis-ci.org/holyshipt/dynamodb_traverse.svg?branch=master"></a>
<a href="https://pypi.org/project/dynamodb-traverse/"><img alt="Build Status" src="https://img.shields.io/pypi/v/dynamodb-traverse?color=green&label=latest"></a>
</p>

### Why manually traverse dynamodb table?
There're tens of ways to consume dynamodb data, for example, dynamodb stream, emr dynamodb connector, kinesis stream... they are good for different use cases. Manual traverse has following benefits comparing to these solutions:
* Deal with "small data"  
* Schema evolution, table migration 
* [Custom TTL mechanism](https://www.linkedin.com/pulse/top-reasons-why-you-should-implement-your-own-ttl-mechanism-he/)
* Full control over offline traversing
* Work with complicated nosql schema 
* Cross AWS account data replication/transformation

### Irrelevant use cases
Since `dynamodb-traverse` is not native to AWS, do not use if your use cases like:
* Real time streaming 
* Simple nosql schema that maps one primary key value to one sort key value
* Big data (~TB) workload that requires dedicated emr clusters
* Data backup

### Installation/Uninstallation
Prerequisite: python 3.8+ and aioboto3>=6.4.1 (bleeding edge)

Run following command to install requirements:

```shell script
$ pip install aioboto3
```

Next, install dynamodb-traverse by running:
```shell script
$ pip install dynamodb-traverse
```

To uninstall dynamodb-traverse, run:
```shell script
$ pip uninstall dynamodb-traverse
```

### Setup
* `dynamodb-traverse` by default looks at `~/.aws/credentials` for profiles you specified in the client. Make sure you have created profile to access dynamodb. 
* You can specify audit log location when initializing client. By default it writes to `/tmp/dynamodb_traverse_xxx.log`.
* We recommend using `35` as default scan batch size because of [dynamodb limitations](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html)

### Benchmark (in progress)
