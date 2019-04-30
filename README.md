# Cloudmesh CLI and REST access to Cloud Data Warehouses


:o: this read me is incomplete

## Motivation

* Understand the construction of REST APIs, and Open API
* Study and Implement microservice architecture 
* Study HTTP performance tools that exist - including some that are cloud based, and some non-cloud based.
* Implement a test driven approach

## Objective

* In the CloudMesh/CMD5 CLI, develop a set of REDSHIFT commands, and commands specific to databases, like REDSHIFT. Examples could to CLUSTER CREATE, CLUSTER DELETE, CLUSTER DESCRIBE, 
* Develop corresponding REST APIs using OpenAPI
* It is demonstarted using redshift

## Introduction to AWS Redshift

RedShift is a Cloud Data Warehouse. It is a managed service, with a multi-node MPP (Massively Parallel Processing) architecture, and capable of scaling to many nodes. 

## Comparable Cloud Data Warehouses
Comparable Cloud Data Warehouses are SnowFlake, and Azure SQL Data Warehouse.

## Getting an AWS account
(todo)
see our manual, you do not have to develop, find link

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

### Creating a demo schema
`cms redshift demoschema db awsuser AWSPass321 cl3.xxxxxx.us-west-2.redshift.amazonaws.com 5439 --createschema`

### Deleting the demo schema
`cms redshift demoschema db awsuser AWSPass321 cl3.xxxxxx.us-west-2.redshift.amazonaws.com 5439 --deleteschema`

### Adding data to the database
Data can be added to the cluster using an import, or running insert statements. 

The demo schema command above also includes some INSERTs to populate the schema tables.

### Querying the data

To query the demo schema table EMP,

`cms redshift runquery db awsuser AWSPass321 cl3.xxxxxx.us-west-2.redshift.amazonaws.com 5439 --empcount`

To run any query on EMP

`cms redshift runquery db awsuser AWSPass321 cl3.ced9iqbk50ks.us-west-2.redshift.amazonaws.com 5439 --querytext='"select empname from emp where empid=20;"'`



## Open API interface (TODO)

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

## Benchmarks

### Benchmarks Commandline Interface

### Benchmarks OpenAPI Interface











