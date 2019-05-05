# Cloudmesh CLI and REST access to Cloud Data Warehouses

## Motivation

* Understand the programmatic interface to AWS RedShift - the cloud datawarehouse from Amazon Web Services
* Understand the construction of REST APIs, and Open API
* Study and implement microservice architecture 
* Implement a test driven approach

## Objective

* In the CloudMesh/CMD5 CLI, develop a set of REDSHIFT commands, and commands specific to databases, like REDSHIFT. Examples could to CLUSTER CREATE, CLUSTER DELETE, CLUSTER DESCRIBE, 
* Develop corresponding REST APIs using OpenAPI
* It is demonstrated using Redshift

## Introduction to AWS Redshift

Redshift is a Cloud Data Warehouse. It is a managed service, with a multi-node MPP (Massively Parallel Processing) architecture, and capable of scaling to many nodes. 

## Comparable Cloud Data Warehouses
Comparable Cloud Data Warehouses are SnowFlake, and Azure SQL Data Warehouse.


## Installation and Setup

You can use pip to install cloudmesh-redshift.

### Install via pip

```bash
$ pip install cloudmesh-cmd5
$ pip install cloudmesh-sys
$ pip install cloudmesh-cloud
$ pip install cloudmesh-redshift
```


### Installing from Source

```bash
$ git clone https://github.com/cloudmesh/cloudmesh-redshift.git
$ cd cloudmesh-redshift
$ pip install -e .
```

The external libraries needed are 
* boto3 : Python AWS library
* psycopg2 : Library to run queries
* base64 : To allow base64 encoding
* docopt : For command line access
* re : For internal parsing

### AWS Account creation and configuration

To create an AWS account refer to [this page](https://cloudmesh.github.io/cloudmesh-manual/accounts/aws.html) from the manual 

To configure Cloudmesh for the AWS account, here are the keys to edit.
Configuration via "~/.cloudmesh/cloudmesh4.yaml"
* cloudmesh.cloud.aws.credentials.EC2_ACCESS_ID
* cloudmesh.cloud.aws.credentials.EC2_SECRET_KEY
* cloudmesh.cloud.aws.credentials.region

### MongoDB dependency
MongoDB is used to store the collections that allow for status passing, results and so on. So, MongoDB will be needed to be started.
```bash
$ cms admin mongo start
```

Here is how to install MongoDB using the cloudmesh shell.
```bash
$ cms admin mongo install
```


## AWS Redshift Usage
This set of interfaces allows you to use AWS Redshift in both admin mode and regular user mode.

### Admin Usage
Admin usage allows you to administer the AWS Redshift cluster
* Create a cluster : 

A single-node or a multi-node cluster may be created.

* Allow external access to the cluster

Networking changes (like allowing port access) are done, to enable access to the AWS Redshift cluster from external programming tools like Python.

* Resize a cluster (nodes) :

Change the number of nodes in the cluster.

* Resize node sizes : 

Alter the sizes of the individual nodes to other sizes  - dc2.large, ds2.xlarge, dc2.8xlarge

* Rename a cluster : 

Change the cluster id for the cluster.

* Change cluster password :

Change the master password of the cluster

### Power user Usage
These are power users who can usage allows for usage of the AWS Redshift cluster.

* Run DDL (Data Definition Language) statements from a file

DDL Statements (like CREATE TABLE, ALTER TABLE, DROP TABLE) can be run from a file.

* Run DML (Data Manipulation Language) statements from a file

DML Statements (like INSERT, UPDATE, DELETE) can be run from a file to insert or alter data in tables in the database.

### User-level Usage
User level usage allows for usage of the AWS Redshift cluster.

* Run Queries against the cluster

SELECT queries to retrieve data from the cluster database can be run from the command line to retrieve data.

`cms redshift runquery db awsuser AWSPass321 cl3.ced9iqbk50ks.us-west-2.redshift.amazonaws.com 5439 --querytext='"select empname from emp where empid=20;"'`


## Command line interface

### Creating a cluster and a database with cms

Here is an example of a single-node cluster

`cms redshift create my-cl1 db1 awsuser AWSPassword321 --nodetype=dc2.large --type=single-node`

Similarly, for multi-node

`cms redshift create my-cl2 db1 awsuser AWSPassword321 --nodetype=dc2.large --type=multi-node --nodes=3`

### Viewing details of the cluster
To view all existing clusters

`cms redshift describe`

To view details of a specific cluster

`cms redshift describe my-cl3`

### Modifying the cluster

#### Changing the password
`cms redshift modify cl11 --newpass MyPassword321`

#### Renaming the cluster
`cms redshift modify cl11 --newid cl12`

#### Resizing the node count
`cms redshift resize my-cl11 --type='multi-node' --nodes=4`

#### Resizing the node types making up the cluster
`cms redshift resize my-cl21 --nodetype='ds2.xlarge' --nodes=2`

### Deleting the cluster
`cms redshift delete my-cl3`

### Defining or altering the schema
'db1','awsuser','AWSPass321','cl8.ced9iqbk50ks.us-west-2.redshift.amazonaws.com',5439,
        #            './redshiftddlfile.sql'
        
### Inserted or modifying the data

'db1','awsuser','AWSPass321','cl8.ced9iqbk50ks.us-west-2.redshift.amazonaws.com',5439,
        #            './redshiftddlfile.sql'
        
### Querying the data

### Creating a demo schema
`cms redshift demoschema db awsuser AWSPass321 cl3.xxxxxx.us-west-2.redshift.amazonaws.com 5439 --createschema`

To query the demo schema table EMP,

`cms redshift runquery db awsuser AWSPass321 cl3.xxxxxx.us-west-2.redshift.amazonaws.com 5439 --empcount`

### Deleting the demo schema
`cms redshift demoschema db awsuser AWSPass321 cl3.xxxxxx.us-west-2.redshift.amazonaws.com 5439 --deleteschema`

## Open API interface

### Creating a cluster and a database with cms APIs

Here is an example of a single-node cluster

`curl -X POST "http://localhost:8080/api/redshift/v1/cluster/cl123?dbName=db1&masterUserName=awsuser1&passWord=AWSPassWord1&nodeType=dc2.large&clusterType=single-node" -H "accept: application/json"`

Similarly, for multi-node

`curl -X POST "http://localhost:8080/api/redshift/v1/cluster/cl123?dbName=db1&masterUserName=awsuser1&passWord=AWSPassWord1&nodeType=dc2.large&clusterType=multi-node&nodeCount=2" -H "accept: application/json"`

### Viewing details of the cluster

To view all existing clusters

`curl -X GET "http://localhost:8080/api/redshift/v1/clusters" -H "accept: application/json"`

To view details of a specific cluster

`curl -X GET "http://localhost:8080/api/redshift/v1/cluster/123" -H "accept: application/json"`

### Modifying the cluster

#### Changing the password

`curl -X PATCH "http://localhost:8080/api/redshift/v1/cluster/cl123/changepassword?newPass=PassAWSword321" -H "accept: application/json"`

#### Renaming the cluster

`curl -X PATCH "http://localhost:8080/api/redshift/v1/cluster/cl123/rename?newId=cl456" -H "accept: application/json"`

#### Resizing the node count

`curl -X PATCH "http://localhost:8080/api/redshift/v1/cluster/cl123/resize?clusterType=multi-node&nodeCount=3&nodeType=dc2.large" -H "accept: application/json"`

#### Resizing the node types making up the cluster

`curl -X PATCH "http://localhost:8080/api/redshift/v1/cluster/cl123/changenodetype?clusterType=multi-node&nodeType=ds2.xlarge" -H "accept: application/json"`

### Deleting a cluster

`curl -X DELETE "http://localhost:8080/api/redshift/v1/cluster/cl123" -H "accept: application/json"`

### Creating a demo schema

`cms redshift demoschema db awsuser AWSPass321 cl3.xxxxxx.us-west-2.redshift.amazonaws.com 5439 --createschema`

### Deleting the demo schema

`cms redshift demoschema db awsuser AWSPass321 cl3.xxxxxx.us-west-2.redshift.amazonaws.com 5439 --deleteschema`

### Adding data to the database (TODO)

Data can be added to the cluster using an import, or running insert statements. 

The demo schema command above also includes some INSERTs to populate the schema tables.

### Querying the data (TODO)

To query the demo schema table EMP,

`cms redshift runquery db awsuser AWSPass321 cl3.xxxxxx.us-west-2.redshift.amazonaws.com 5439 --empcount`

To run any query on EMP

`cms redshift runquery db awsuser AWSPass321 cl3.ced9iqbk50ks.us-west-2.redshift.amazonaws.com 5439 --querytext='"select empname from emp where empid=20;

## Suggested security levels

As mentioned above, there are typically 3 levels to the interface

* Admin level
* Power user level
* User level

Security for these APIs can be granted accordingly.

For most of the Cluster operations and DDL (Schema operations), it is suggested that the swagger API would have some "admin" level security.

For example

````  
      security:
        - OAuth2: [admin]   # Use OAuth with a different scope
      responses:
        '200':
          description: OK
        '401':
          description: Not authenticated
        '403':
          description: Access token does not have the required scope
````

## Benchmarks

### Benchmarks Commandline Interface


#### Create the cluster
```
+------------------+--------------------------------------------------------------------------------------------------+
| Machine Arribute | Time/s                                                                                           |
+------------------+--------------------------------------------------------------------------------------------------+
| mac_version      | 10.14.4                                                                                          |
| machine          | ('x86_64',)                                                                                      |
| node             | ('USL012826',)                                                                                   |
| platform         | Darwin-18.5.0-x86_64-i386-64bit                                                                  |
| processor        | ('i386',)                                                                                        |
| processors       | Darwin                                                                                           |
| python           | 3.7.2 (default, Apr 11 2019, 21:32:35)                                                           |
|                  | [Clang 10.0.1 (clang-1001.0.46.3)]                                                               |
| release          | ('18.5.0',)                                                                                      |
| sys              | darwin                                                                                           |
| system           | Darwin                                                                                           |
| user             | shirish_joshi                                                                                    |
| version          | Darwin Kernel Version 18.5.0: Mon Mar 11 20:40:32 PDT 2019; root:xnu-4903.251.3~3/RELEASE_X86_64 |
| win_version      |                                                                                                  |
+------------------+--------------------------------------------------------------------------------------------------+
+------------------------------------------+------+----------------+--------+-------------+-------------+
| timer                                    | time | node           | system | mac_version | win_version |
+------------------------------------------+------+----------------+--------+-------------+-------------+
| cms redshift create my-cl1 db1 awsuser   | 3.72 | ('USL012826',) | Darwin | 10.14.4     |             |
| AWSPass321 --nodetype=dc2.large          |      |                |        |             |             |
| --type=single-node                       |      |                |        |             |             |
+------------------------------------------+------+----------------+--------+-------------+-------------+
```


```
+------------------+--------------------------------------------------------------------------------------------------+
| Machine Arribute | Time/s                                                                                           |
+------------------+--------------------------------------------------------------------------------------------------+
| mac_version      | 10.14.4                                                                                          |
| machine          | ('x86_64',)                                                                                      |
| node             | ('USL012826',)                                                                                   |
| platform         | Darwin-18.5.0-x86_64-i386-64bit                                                                  |
| processor        | ('i386',)                                                                                        |
| processors       | Darwin                                                                                           |
| python           | 3.7.2 (default, Apr 11 2019, 21:32:35)                                                           |
|                  | [Clang 10.0.1 (clang-1001.0.46.3)]                                                               |
| release          | ('18.5.0',)                                                                                      |
| sys              | darwin                                                                                           |
| system           | Darwin                                                                                           |
| user             | shirish_joshi                                                                                    |
| version          | Darwin Kernel Version 18.5.0: Mon Mar 11 20:40:32 PDT 2019; root:xnu-4903.251.3~3/RELEASE_X86_64 |
| win_version      |                                                                                                  |
+------------------+--------------------------------------------------------------------------------------------------+
+------------------------------------------+------+----------------+--------+-------------+-------------+
| timer                                    | time | node           | system | mac_version | win_version |
+------------------------------------------+------+----------------+--------+-------------+-------------+
| cms redshift create my-cl2 db1 awsuser   | 3.78 | ('USL012826',) | Darwin | 10.14.4     |             |
| AWSPass321 --nodetype=dc2.large          |      |                |        |             |             |
| --type=multi-node --nodes=2              |      |                |        |             |             |
+------------------------------------------+------+----------------+--------+-------------+-------------+
```


#### Describe Clusters

```
+------------------+--------------------------------------------------------------------------------------------------+
| Machine Arribute | Time/s                                                                                           |
+------------------+--------------------------------------------------------------------------------------------------+
| mac_version      | 10.14.4                                                                                          |
| machine          | ('x86_64',)                                                                                      |
| node             | ('USL012826',)                                                                                   |
| platform         | Darwin-18.5.0-x86_64-i386-64bit                                                                  |
| processor        | ('i386',)                                                                                        |
| processors       | Darwin                                                                                           |
| python           | 3.7.2 (default, Apr 11 2019, 21:32:35)                                                           |
|                  | [Clang 10.0.1 (clang-1001.0.46.3)]                                                               |
| release          | ('18.5.0',)                                                                                      |
| sys              | darwin                                                                                           |
| system           | Darwin                                                                                           |
| user             | shirish_joshi                                                                                    |
| version          | Darwin Kernel Version 18.5.0: Mon Mar 11 20:40:32 PDT 2019; root:xnu-4903.251.3~3/RELEASE_X86_64 |
| win_version      |                                                                                                  |
+------------------+--------------------------------------------------------------------------------------------------+
+-------------------+------+----------------+--------+-------------+-------------+
| timer             | time | node           | system | mac_version | win_version |
+-------------------+------+----------------+--------+-------------+-------------+
| describe clusters | 1.08 | ('USL012826',) | Darwin | 10.14.4     |             |
+-------------------+------+----------------+--------+-------------+-------------+
```

```
+------------------+--------------------------------------------------------------------------------------------------+
| Machine Arribute | Time/s                                                                                           |
+------------------+--------------------------------------------------------------------------------------------------+
| mac_version      | 10.14.4                                                                                          |
| machine          | ('x86_64',)                                                                                      |
| node             | ('USL012826',)                                                                                   |
| platform         | Darwin-18.5.0-x86_64-i386-64bit                                                                  |
| processor        | ('i386',)                                                                                        |
| processors       | Darwin                                                                                           |
| python           | 3.7.2 (default, Apr 11 2019, 21:32:35)                                                           |
|                  | [Clang 10.0.1 (clang-1001.0.46.3)]                                                               |
| release          | ('18.5.0',)                                                                                      |
| sys              | darwin                                                                                           |
| system           | Darwin                                                                                           |
| user             | shirish_joshi                                                                                    |
| version          | Darwin Kernel Version 18.5.0: Mon Mar 11 20:40:32 PDT 2019; root:xnu-4903.251.3~3/RELEASE_X86_64 |
| win_version      |                                                                                                  |
+------------------+--------------------------------------------------------------------------------------------------+
+---------------------------+------+----------------+--------+-------------+-------------+
| timer                     | time | node           | system | mac_version | win_version |
+---------------------------+------+----------------+--------+-------------+-------------+
| cms redshift describe cl9 | 3.22 | ('USL012826',) | Darwin | 10.14.4     |             |
+---------------------------+------+----------------+--------+-------------+-------------+
```


#### Allow access to the DB

```
+------------------+--------------------------------------------------------------------------------------------------+
| Machine Arribute | Time/s                                                                                           |
+------------------+--------------------------------------------------------------------------------------------------+
| mac_version      | 10.14.4                                                                                          |
| machine          | ('x86_64',)                                                                                      |
| node             | ('USL012826',)                                                                                   |
| platform         | Darwin-18.5.0-x86_64-i386-64bit                                                                  |
| processor        | ('i386',)                                                                                        |
| processors       | Darwin                                                                                           |
| python           | 3.7.2 (default, Apr 11 2019, 21:32:35)                                                           |
|                  | [Clang 10.0.1 (clang-1001.0.46.3)]                                                               |
| release          | ('18.5.0',)                                                                                      |
| sys              | darwin                                                                                           |
| system           | Darwin                                                                                           |
| user             | shirish_joshi                                                                                    |
| version          | Darwin Kernel Version 18.5.0: Mon Mar 11 20:40:32 PDT 2019; root:xnu-4903.251.3~3/RELEASE_X86_64 |
| win_version      |                                                                                                  |
+------------------+--------------------------------------------------------------------------------------------------+
+------------------------------+------+----------------+--------+-------------+-------------+
| timer                        | time | node           | system | mac_version | win_version |
+------------------------------+------+----------------+--------+-------------+-------------+
| cms redshift allowaccess cl8 | 4.83 | ('USL012826',) | Darwin | 10.14.4     |             |
+------------------------------+------+----------------+--------+-------------+-------------+
```



#### Modify the cluster

```
+------------------+--------------------------------------------------------------------------------------------------+
| Machine Arribute | Time/s                                                                                           |
+------------------+--------------------------------------------------------------------------------------------------+
| mac_version      | 10.14.4                                                                                          |
| machine          | ('x86_64',)                                                                                      |
| node             | ('USL012826',)                                                                                   |
| platform         | Darwin-18.5.0-x86_64-i386-64bit                                                                  |
| processor        | ('i386',)                                                                                        |
| processors       | Darwin                                                                                           |
| python           | 3.7.2 (default, Apr 11 2019, 21:32:35)                                                           |
|                  | [Clang 10.0.1 (clang-1001.0.46.3)]                                                               |
| release          | ('18.5.0',)                                                                                      |
| sys              | darwin                                                                                           |
| system           | Darwin                                                                                           |
| user             | shirish_joshi                                                                                    |
| version          | Darwin Kernel Version 18.5.0: Mon Mar 11 20:40:32 PDT 2019; root:xnu-4903.251.3~3/RELEASE_X86_64 |
| win_version      |                                                                                                  |
+------------------+--------------------------------------------------------------------------------------------------+
+------------------------------+------+----------------+--------+-------------+-------------+
| timer                        | time | node           | system | mac_version | win_version |
+------------------------------+------+----------------+--------+-------------+-------------+
| resize cluster to multi node | 1.38 | ('USL012826',) | Darwin | 10.14.4     |             |
+------------------------------+------+----------------+--------+-------------+-------------+
```


```
+------------------+--------------------------------------------------------------------------------------------------+
| Machine Arribute | Time/s                                                                                           |
+------------------+--------------------------------------------------------------------------------------------------+
| mac_version      | 10.14.4                                                                                          |
| machine          | ('x86_64',)                                                                                      |
| node             | ('USL012826',)                                                                                   |
| platform         | Darwin-18.5.0-x86_64-i386-64bit                                                                  |
| processor        | ('i386',)                                                                                        |
| processors       | Darwin                                                                                           |
| python           | 3.7.2 (default, Apr 11 2019, 21:32:35)                                                           |
|                  | [Clang 10.0.1 (clang-1001.0.46.3)]                                                               |
| release          | ('18.5.0',)                                                                                      |
| sys              | darwin                                                                                           |
| system           | Darwin                                                                                           |
| user             | shirish_joshi                                                                                    |
| version          | Darwin Kernel Version 18.5.0: Mon Mar 11 20:40:32 PDT 2019; root:xnu-4903.251.3~3/RELEASE_X86_64 |
| win_version      |                                                                                                  |
+------------------+--------------------------------------------------------------------------------------------------+
+------------------------------------------+------+----------------+--------+-------------+-------------+
| timer                                    | time | node           | system | mac_version | win_version |
+------------------------------------------+------+----------------+--------+-------------+-------------+
| cms redshift modify cl9 --newpass        | 3.73 | ('USL012826',) | Darwin | 10.14.4     |             |
| MyNewPass321                             |      |                |        |             |             |
+------------------------------------------+------+----------------+--------+-------------+-------------+
```

#### Change the cluster ID

```
+------------------+--------------------------------------------------------------------------------------------------+
| Machine Arribute | Time/s                                                                                           |
+------------------+--------------------------------------------------------------------------------------------------+
| mac_version      | 10.14.4                                                                                          |
| machine          | ('x86_64',)                                                                                      |
| node             | ('USL012826',)                                                                                   |
| platform         | Darwin-18.5.0-x86_64-i386-64bit                                                                  |
| processor        | ('i386',)                                                                                        |
| processors       | Darwin                                                                                           |
| python           | 3.7.2 (default, Apr 11 2019, 21:32:35)                                                           |
|                  | [Clang 10.0.1 (clang-1001.0.46.3)]                                                               |
| release          | ('18.5.0',)                                                                                      |
| sys              | darwin                                                                                           |
| system           | Darwin                                                                                           |
| user             | shirish_joshi                                                                                    |
| version          | Darwin Kernel Version 18.5.0: Mon Mar 11 20:40:32 PDT 2019; root:xnu-4903.251.3~3/RELEASE_X86_64 |
| win_version      |                                                                                                  |
+------------------+--------------------------------------------------------------------------------------------------+
+-------------------------------------+------+----------------+--------+-------------+-------------+
| timer                               | time | node           | system | mac_version | win_version |
+-------------------------------------+------+----------------+--------+-------------+-------------+
| cms redshift modify cl8 --newid cl9 | 3.34 | ('USL012826',) | Darwin | 10.14.4     |             |
+-------------------------------------+------+----------------+--------+-------------+-------------+
```

#### Run DDL against the DB

```
+------------------+--------------------------------------------------------------------------------------------------+
| Machine Arribute | Time/s                                                                                           |
+------------------+--------------------------------------------------------------------------------------------------+
| mac_version      | 10.14.4                                                                                          |
| machine          | ('x86_64',)                                                                                      |
| node             | ('USL012826',)                                                                                   |
| platform         | Darwin-18.5.0-x86_64-i386-64bit                                                                  |
| processor        | ('i386',)                                                                                        |
| processors       | Darwin                                                                                           |
| python           | 3.7.2 (default, Apr 11 2019, 21:32:35)                                                           |
|                  | [Clang 10.0.1 (clang-1001.0.46.3)]                                                               |
| release          | ('18.5.0',)                                                                                      |
| sys              | darwin                                                                                           |
| system           | Darwin                                                                                           |
| user             | shirish_joshi                                                                                    |
| version          | Darwin Kernel Version 18.5.0: Mon Mar 11 20:40:32 PDT 2019; root:xnu-4903.251.3~3/RELEASE_X86_64 |
| win_version      |                                                                                                  |
+------------------+--------------------------------------------------------------------------------------------------+
+------------------------------------------+------+----------------+--------+-------------+-------------+
| timer                                    | time | node           | system | mac_version | win_version |
+------------------------------------------+------+----------------+--------+-------------+-------------+
| cms redshift runddl db1 awsuser          | 4.21 | ('USL012826',) | Darwin | 10.14.4     |             |
| AWSPass321 cl8.ced9iqbk50ks.us-          |      |                |        |             |             |
| west-2.redshift.amazonaws.com 5439       |      |                |        |             |             |
| --ddlfile=./redshiftddlfile.sql          |      |                |        |             |             |
+------------------------------------------+------+----------------+--------+-------------+-------------+
```


#### Run DML against the DB

```
+------------------+--------------------------------------------------------------------------------------------------+
| Machine Arribute | Time/s                                                                                           |
+------------------+--------------------------------------------------------------------------------------------------+
| mac_version      | 10.14.4                                                                                          |
| machine          | ('x86_64',)                                                                                      |
| node             | ('USL012826',)                                                                                   |
| platform         | Darwin-18.5.0-x86_64-i386-64bit                                                                  |
| processor        | ('i386',)                                                                                        |
| processors       | Darwin                                                                                           |
| python           | 3.7.2 (default, Apr 11 2019, 21:32:35)                                                           |
|                  | [Clang 10.0.1 (clang-1001.0.46.3)]                                                               |
| release          | ('18.5.0',)                                                                                      |
| sys              | darwin                                                                                           |
| system           | Darwin                                                                                           |
| user             | shirish_joshi                                                                                    |
| version          | Darwin Kernel Version 18.5.0: Mon Mar 11 20:40:32 PDT 2019; root:xnu-4903.251.3~3/RELEASE_X86_64 |
| win_version      |                                                                                                  |
+------------------+--------------------------------------------------------------------------------------------------+
+------------------------------------------+------+----------------+--------+-------------+-------------+
| timer                                    | time | node           | system | mac_version | win_version |
+------------------------------------------+------+----------------+--------+-------------+-------------+
| cms redshift rundml db1 awsuser          | 3.19 | ('USL012826',) | Darwin | 10.14.4     |             |
| AWSPass321 cl8.ced9iqbk50ks.us-          |      |                |        |             |             |
| west-2.redshift.amazonaws.com 5439       |      |                |        |             |             |
| --dmlfile=./redshiftdmlfile.sql          |      |                |        |             |             |
+------------------------------------------+------+----------------+--------+-------------+-------------+
```

#### Run SELECT against the DB

```
+------------------+--------------------------------------------------------------------------------------------------+
| Machine Arribute | Time/s                                                                                           |
+------------------+--------------------------------------------------------------------------------------------------+
| mac_version      | 10.14.4                                                                                          |
| machine          | ('x86_64',)                                                                                      |
| node             | ('USL012826',)                                                                                   |
| platform         | Darwin-18.5.0-x86_64-i386-64bit                                                                  |
| processor        | ('i386',)                                                                                        |
| processors       | Darwin                                                                                           |
| python           | 3.7.2 (default, Apr 11 2019, 21:32:35)                                                           |
|                  | [Clang 10.0.1 (clang-1001.0.46.3)]                                                               |
| release          | ('18.5.0',)                                                                                      |
| sys              | darwin                                                                                           |
| system           | Darwin                                                                                           |
| user             | shirish_joshi                                                                                    |
| version          | Darwin Kernel Version 18.5.0: Mon Mar 11 20:40:32 PDT 2019; root:xnu-4903.251.3~3/RELEASE_X86_64 |
| win_version      |                                                                                                  |
+------------------+--------------------------------------------------------------------------------------------------+
+------------------------------------------+------+----------------+--------+-------------+-------------+
| timer                                    | time | node           | system | mac_version | win_version |
+------------------------------------------+------+----------------+--------+-------------+-------------+
| cms redshift runquery db1 awsuser        | 0.04 | ('USL012826',) | Darwin | 10.14.4     |             |
| AWSPass321 cl8.ced9iqbk50ks.us-          |      |                |        |             |             |
| west-2.redshift.amazonaws.com 5439       |      |                |        |             |             |
| --querytext='"select empname from emp whe|      |                |        |             |             |
| re empid=20;"'                           |      |                |        |             |             |  
+------------------------------------------+------+----------------+--------+-------------+-------------+
```



### Benchmarks OpenAPI Interface











