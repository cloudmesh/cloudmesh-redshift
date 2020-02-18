###############################################################
# pytest -v --capture=no tests/test_redshift_openapi.py
# pytest -v  tests/test_redshift_openapi.py
# pytest -v --capture=no -v --nocapture tests/test_redshift_openapi..py::Test_RedShift_openapi::<METHODNAME>
###############################################################
from cloudmesh.management.configuration.config import Config
from cloudmesh.common.run.subprocess import run
# import cloudmesh.redshift.command.run
from cloudmesh.common.StopWatch import StopWatch


import pytest


def run_curl(command):
    StopWatch.start(command)
    output = run(['curl', command], shell=False)
    StopWatch.stop(command)
    return output


@pytest.mark.incremental
class Test_RedShift_openapi:

    def setup(self):
        self.clusterid = ""

    def test_describe_clusters(self):
        result = run_curl('http://localhost:8080/api/redshift/v1/clusters')

        assert result is not None
        assert result[0] == "["

    def test_describe_cluster(self):
        result = run_curl('https://localhost:8080/api/redshift/v1/cluster/123')

        assert result is not None
        assert result[0] == "{"

    def test_create_single_node_cluster(self):
        result = run_curl('https://localhost:8080/api/redshift/v1/cluster/123?dbName=db1&masterUserName=awsuser1&passWord=AWSPassWord1&nodeType=dc2.large&clusterType=single-node')

        assert result is not None
        assert result[0] == "{"

    def test_create_multi_node_cluster(self):
        result = run_curl('https://localhost:8080/api/redshift/v1/cluster/123?dbName=db1&masterUserName=awsuser1&passWord=AWSPassWord1&nodeType=dc2.large&clusterType=multi-node&nodeCount=2')

        assert result is not None
        assert result[0] == "{"

    def test_delete_cluster(self):
        result = run_curl('http://localhost:8080/api/redshift/v1/cluster/123')

        assert result is not None
        assert result[0] == "{"

    def test_resize_cluster_node_types(self):
        result = run_curl('http://localhost:8080/api/redshift/v1/cluster/123/changenodetype?clusterType=multi-node&nodeType=dc2.large')

        assert result is not None
        assert result[0] == "{"

    def test_resize_cluster_to_multi_node(self):
        result = run_curl('http://localhost:8080/api/redshift/v1/cluster/123/resize?clusterType=multi-node&nodeCount=2&nodeType=dc2.large')

        assert result is not None
        assert result[0] == "{"

    def test_modify_cluster(self):
        result = run_curl('http://localhost:8080/api/redshift/v1/cluster/123/changenodetype?clusterType=multi-node&nodeType=dc2.large')

        assert result is not None
        assert result[0] == "{"

    def test_rename_cluster(self):
        result = run_curl('http://localhost:8080/api/redshift/v1/cluster/123/rename?newId=456')

        assert result is not None
        assert result[0] == "{"

    def test_allow_access(self):
        result = run_curl('http://localhost:8080/cloudmesh/redshift/v1/cluster/cl123/allowaccess')

        assert result is not None
        assert result[0] == "{"

    def test_run_ddl(self):
        result = run_curl('http://localhost:8080/cloudmesh/redshift/v1/cluster/cl123/runDDL?dbName=db1&host=cl8.ced9iqbk50ks.us-west-2.redshift.amazonaws.com&port=5439&userName=awsuser&passWord=AWSPass123&sql_file_contents=Q1JFQVRFIFRBQkxFIEVNUChFTVBfSUQgSU5ULCBFTVBfTkFNRSBWQVJDSEFSKDEyMCkpOwpDUkVBVEUgVEFCTEUgREVQVCAoREVQVF9JRCBJTlQsIEROQU1FIFZBUkNIQVIoODApKTsKQ1JFQVRFIFRBQkxFIEFTU0lHTiAoRU1QSUQgSU5ULCBERVBUX0lEIElOVCk7Cg%3D%3D')

        assert result is not None
        assert result[0] == "{"

    def test_run_dml(self):
        result = run_curl('http://localhost:8080/cloudmesh/redshift/v1/cluster/cl123/runDML?dbName=db1&host=cl8.ced9iqbk50ks.us-west-2.redshift.amazonaws.com&port=5439&userName=awsuser&passWord=AWSPass123&sql_file_contents=SU5TRVJUIElOVE8gRU1QIFZBTFVFUyAoMTAsICdzbWl0aCcpOwpJTlNFUlQgSU5UTyBFTVAgVkFMVUVTICgyMCwgJ2pvbmVzJyk7CklOU0VSVCBJTlRPIEVNUCBWQUxVRVMgKDMwLCAnc2NvdHQnKTsKCg%3D%3D')

        assert result is not None
        assert result[0] == "{"

    def test_run_select_query(self):
        result = run_curl('http://localhost:8080/cloudmesh/redshift/v1/cluster/cl8/runQuery?dbName=db1&host=cl8.ced9iqbk50ks.us-west-2.redshift.amazonaws.com&port=5439&userName=awsuser&passWord=AWSPass123&queryText=SELECT%20count(*)%20from%20EMP%3B')

        assert result is not None
        assert result[0] == "{"

    def test_benchmark(self):

        StopWatch.benchmark()


if __name__ == "__main__":
    print("In test_redshift_api")
    t = Test_RedShift_openapi()

    StopWatch.benchmark()
