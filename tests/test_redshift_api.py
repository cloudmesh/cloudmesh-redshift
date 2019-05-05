###############################################################
# pytest -v --capture=no tests/test_redshift_openapi.py
# pytest -v  tests/test_redshift_openapi.py
# pytest -v --capture=no -v --nocapture tests/test_redshift_openapi.py:Test_RedShift_openapi.<METHODNAME>
###############################################################
from cloudmesh.management.configuration.config import Config
from cloudmesh.common.run.subprocess import run
import cloudmesh.redshift.command.run



import pytest


@pytest.mark.incremental
class Test_RedShift_openapi:

    def setup(self):
        self.clusterid = ""

    def test_describe_clusters(self):
        result = run(['curl', 'http://localhost:8080/api/redshift/v1/clusters'], shell=False)

        assert result is not None
        assert result[0] == "["

    def test_describe_cluster(self):
        result = run(['curl', 'https://localhost:8080/api/redshift/v1/cluster/123'], shell=False)

        assert result is not None
        assert result[0] == "{"

    def test_create_single_node_cluster(self):
        result = run(['curl', 'https://localhost:8080/api/redshift/v1/cluster/123?dbName=db1&masterUserName=awsuser1&passWord=AWSPassWord1&nodeType=dc2.large&clusterType=single-node'],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

    def test_create_multi_node_cluster(self):
        result = run(['curl', 'https://localhost:8080/api/redshift/v1/cluster/123?dbName=db1&masterUserName=awsuser1&passWord=AWSPassWord1&nodeType=dc2.large&clusterType=multi-node&nodeCount=2'],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

    def test_delete_cluster(self):
        result = run(['curl','http://localhost:8080/api/redshift/v1/cluster/123'], shell=False)

        assert result is not None
        assert result[0] == "{"

    def test_resize_cluster_node_types(self):
        result = run(['curl','http://localhost:8080/api/redshift/v1/cluster/123/changenodetype?clusterType=multi-node&nodeType=dc2.large'], shell=False)

        assert result is not None
        assert result[0] == "{"

    def test_resize_cluster_to_multi_node(self):
        result = run(['curl', 'http://localhost:8080/api/redshift/v1/cluster/123/resize?clusterType=multi-node&nodeCount=2&nodeType=dc2.large'],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

    def test_modify_cluster(self):
        result = run(['curl', 'http://localhost:8080/api/redshift/v1/cluster/123/changenodetype?clusterType=multi-node&nodeType=dc2.large'],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

        self.clusterid = ""


    def test_rename_cluster(self):
        result = run(['curl', 'http://localhost:8080/api/redshift/v1/cluster/123/rename?newId=456'],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

        self.clusterid = ""


    def test_allow_access(self):
        result = run(['curl', 'http://localhost:8080/cloudmesh/redshift/v1/cluster/cl123/allowaccess'],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

        self.clusterid = ""


    def test_run_ddl(self):
        result = run(['curl', 'http://localhost:8080/cloudmesh/redshift/v1/cluster/cl123/runDDL?dbName=db1&host=cl8.ced9iqbk50ks.us-west-2.redshift.amazonaws.com&port=5439&userName=awsuser&passWord=AWSPass123&sql_file_contents=Q1JFQVRFIFRBQkxFIEVNUChFTVBfSUQgSU5ULCBFTVBfTkFNRSBWQVJDSEFSKDEyMCkpOwpDUkVBVEUgVEFCTEUgREVQVCAoREVQVF9JRCBJTlQsIEROQU1FIFZBUkNIQVIoODApKTsKQ1JFQVRFIFRBQkxFIEFTU0lHTiAoRU1QSUQgSU5ULCBERVBUX0lEIElOVCk7Cg%3D%3D'],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

        self.clusterid = ""


    def test_run_dml(self):
        result = run(['curl', 'http://localhost:8080/cloudmesh/redshift/v1/cluster/cl123/runDML?dbName=db1&host=cl8.ced9iqbk50ks.us-west-2.redshift.amazonaws.com&port=5439&userName=awsuser&passWord=AWSPass123&sql_file_contents=SU5TRVJUIElOVE8gRU1QIFZBTFVFUyAoMTAsICdzbWl0aCcpOwpJTlNFUlQgSU5UTyBFTVAgVkFMVUVTICgyMCwgJ2pvbmVzJyk7CklOU0VSVCBJTlRPIEVNUCBWQUxVRVMgKDMwLCAnc2NvdHQnKTsKCg%3D%3D'],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

        self.clusterid = ""


    def test_run_select_query(self):
        result = run(['curl', 'http://localhost:8080/cloudmesh/redshift/v1/cluster/cl8/runQuery?dbName=db1&host=cl8.ced9iqbk50ks.us-west-2.redshift.amazonaws.com&port=5439&userName=awsuser&passWord=AWSPass123&queryText=SELECT%20count(*)%20from%20EMP%3B'],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

        self.clusterid = ""
