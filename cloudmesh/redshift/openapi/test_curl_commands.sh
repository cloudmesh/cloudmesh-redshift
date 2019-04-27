curl -X GET "http://localhost:8080/api/redshift/v1/clusters" -H "accept: application/json"

curl -X GET "http://localhost:8080/api/redshift/v1/cluster/123" -H "accept: application/json"

curl -X POST "http://localhost:8080/api/redshift/v1/cluster/123?dbName=db1&masterUserName=awsuser1&passWord=AWSPassWord1&nodeType=dc2.large&clusterType=multi-node&nodeCount=2" -H "accept: application/json"

curl -X DELETE "http://localhost:8080/api/redshift/v1/cluster/123" -H "accept: application/json"

curl -X PATCH "http://localhost:8080/api/redshift/v1/cluster/123/resize?clusterType=multi-node&nodeCount=2&nodeType=dc2.large" -H "accept: application/json"

curl -X PATCH "http://localhost:8080/api/redshift/v1/cluster/123/changenodetype?clusterType=multi-node&nodeType=dc2.large" -H "accept: application/json"

curl -X PATCH "http://localhost:8080/api/redshift/v1/cluster/123/rename?newId=456" -H "accept: application/json"

curl -X PATCH "http://localhost:8080/api/redshift/v1/cluster/123/changepassword?newPass=PassAWSword321" -H "accept: application/json"