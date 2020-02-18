###############################################################
# pytest -v --capture=no tests/test_redshift_manager.py
# pytest -v  tests/test_redshift_manager.py
# pytest -v --capture=no -v --nocapture tests/test_redshift_manager..py::TestRedshiftAPIProvider::<METHODNAME>
###############################################################

from cloudmesh.redshift.Provider import Provider
from cloudmesh.common.StopWatch import StopWatch
import pytest
import boto3
import base64

import shutil
import os
from cloudmesh_installer.install.test import readfile, run


@pytest.mark.incremental
class TestRedshiftAPIProvider():
    def t1_get_client(self):
        pass

    # @pytest.mark.skip(reason="no way of currently testing this")
    def t1_describe_clusters(self):
        StopWatch.start("describe clusters")
        m = Provider()
        r = m.describe_clusters()
        StopWatch.stop("describe clusters")
        print(r)
        assert True

    def t1_describe_cluster(self, cluster_id='my-cl1'):
        StopWatch.start("describe named cluster")
        m = Provider()
        r = m.describe_cluster(cluster_id)
        StopWatch.stop("describe named cluster")
        print(r)
        assert True

    def t1_create_single_node_cluster(self, db_name='db1', cluster_id='my-cl1', cluster_type='single-node', node_type='dc2.large', user_name='awsuser', passwd='AWSPass321'):
        StopWatch.start("create single node cluster")
        m = Provider()

        r = m.create_single_node_cluster(db_name, cluster_id, cluster_type, node_type, user_name, passwd)
        StopWatch.stop("create single node cluster")
        print(r)
        assert True

    def t1_create_multi_node_cluster(self, db_name='db1', cluster_id='my-cl1', cluster_type='single-node', node_type='dc2.large', user_name='awsuser', passwd='AWSPass321', node_count=2):
        StopWatch.start("create multi node cluster")
        m = Provider()
        r = m.create_multi_node_cluster(db_name, cluster_id, cluster_type, node_type, user_name, passwd, node_count)
        StopWatch.stop("create multi node cluster")
        print(r)
        assert True

    def t1_delete_cluster(self, cluster_id='my-cl1'):
        StopWatch.start("delete cluster")
        m = Provider()
        r = m.delete_cluster(cluster_id)
        StopWatch.stop("delete cluster")
        print(r)
        assert True

    def t1_resize_cluster_node_types(self, cluster_id='my-cl1', node_type='ds2.xlarge', node_count=2):
        StopWatch.start("resize cluster node types")
        m = Provider()
        r = m.resize_cluster_node_types(cluster_id, node_type, node_count)
        StopWatch.stop("resize cluster node types")
        print(r)
        assert True

    # def t1_resize_cluster_node_count(self, cluster_id='my-cl1', cluster_type='multi-node', node_count=2):
    #     StopWatch.start("resize cluster node count")
    #     m = Provider()
    #     r = m.resize_cluster_node_count(cluster_id, cluster_type, node_count)
    #     StopWatch.stop("resize cluster node count")
    #     print(r)
    #     assert True

    def t1_resize_cluster_to_multi_node(self, cluster_id='my-cl1', cluster_type='multi-node', node_count=2, node_type='dc2.large'):
        StopWatch.start("resize cluster to multi node")
        m = Provider()
        r = m.resize_cluster_to_multi_node(cluster_id, cluster_type, node_count, node_type)
        StopWatch.stop("resize cluster to multi node")
        print(r)
        assert True

    def t1_modify_cluster(self, cluster_id='my-cl1', new_pass='AWSPassword123'):
        StopWatch.start("modify cluster")
        m = Provider()
        r = m.modify_cluster(cluster_id, new_pass)
        StopWatch.stop("modify cluster")
        print(r)
        assert True

    def t1_rename_cluster(self, cluster_id='my-cl1', new_id='my=cl111'):
        StopWatch.start("rename cluster")
        m = Provider()
        r = m.rename_cluster(cluster_id, new_id)
        StopWatch.stop("rename cluster")
        print(r)
        assert True

    def t1_allow_access(self, cluster_id='my-cl1'):
        StopWatch.start("allow access")
        m = Provider()
        r = m.allow_access(cluster_id)
        StopWatch.stop("allow access")
        print(r)
        assert True

    def t1_run_ddl(self, cluster_id='my-cl1', db_name='db1', host='my-cl1.ced9iqbk50ks.us-west-2.redshift.amazonaws.com',
                   port=5439, user_name='awsuser', passwd='AWSPass321', ddl_file='./redshiftddlfile.sql'):
        fd = open(ddl_file, 'r')
        ddl_file_contents = fd.read()
        fd.close()
        b64_sql_file_contents = base64.b64encode(bytes(ddl_file_contents, 'ascii'))

        StopWatch.start("run ddl")
        m = Provider()
        r = m.runddl(cluster_id, db_name, host, port, user_name, passwd, b64_sql_file_contents)
        StopWatch.stop("run ddl")
        print(r)
        assert True

    def t1_run_dml(self, cluster_id='my-cl1', db_name='db1', host='my-cl1.ced9iqbk50ks.us-west-2.redshift.amazonaws.com',
                   port=5439, user_name='awsuser', passwd='AWSPass321', dml_file='./redshiftdmlfile.sql'):
        fd = open(dml_file, 'r')
        dml_file_contents = fd.read()
        fd.close()
        b64_sql_file_contents = base64.b64encode(bytes(dml_file_contents, 'ascii'))

        StopWatch.start("run dml")
        m = Provider()
        r = m.rundml(cluster_id, db_name, host, port, user_name, passwd, b64_sql_file_contents)
        StopWatch.stop("run dml")
        print(r)
        assert True

    def t1_run_select_query(self, cluster_id='my-cl1', db_name='db1', host='my-cl1.ced9iqbk50ks.us-west-2.redshift.amazonaws.com', port=5439, user_name='awsuser', passwd='AWSPass321', query_text="SELECT COUNT(*) FROM emp"):
        StopWatch.start("run select")
        m = Provider()
        r = m.runselectquery_text(cluster_id, db_name, host, port, user_name, passwd, query_text)
        StopWatch.stop("run select")
        print(r)
        assert True

    # def test_mongo(self):
    #     print("In Mongo")
    #     m = Provider()
    #     m.update_dict()
    #     pass


    def test_benchmark(self):
        t = TestRedshiftAPIProvider()
        # t.t1_describe_clusters()
        # t.t1_describe_cluster('cl6')
        # t.t1_create_single_node_cluster('db1', 'my-cl1','single-node','dc2.large','awsuser','AWSPass321')

        # t.t1_create_multi_node_cluster('db1', 'my-cl2','multi-node','dc2.large','awsuser','AWSPass321',2)

        # t.t1_create_single_node_cluster('db1', 'my-cl7','single-node','dc2.large','awsuser','AWSPass321')
        # t.t1_create_multi_node_cluster('db1', 'my-cl2','multi-node','dc2.large','awsuser','AWSPass321',2)

        # t.t1_allow_access('my-cl7')

        #t.t1_run_select_query(host='my-cl7.ced9iqbk50ks.us-west-2.redshift.amazonaws.com')

        #t.t1_run_ddl('my-cl7',db_name='db1',host='my-cl7.ced9iqbk50ks.us-west-2.redshift.amazonaws.com',port=5439, user_name='awsuser', passwd='AWSPass321', ddl_file="./redshiftddlfile.sql")

        #t.t1_run_dml('my-cl7',db_name='db1',host='my-cl7.ced9iqbk50ks.us-west-2.redshift.amazonaws.com',port=5439, user_name='awsuser', passwd='AWSPass321', dml_file="./redshiftdmlfile.sql")

        #t.t1_run_select_query(host='my-cl7.ced9iqbk50ks.us-west-2.redshift.amazonaws.com')

        t.t1_describe_clusters()

        StopWatch.benchmark()


if __name__ == "__main__":
    print("In test_manager")
    t = TestRedshiftAPIProvider()
    # t.t1_describe_clusters()
    # t.t1_describe_cluster('cl6')
    # t.t1_create_single_node_cluster('db1', 'my-cl1','single-node','dc2.large','awsuser','AWSPass321')

    # t.t1_create_multi_node_cluster('db1', 'my-cl2','multi-node','dc2.large','awsuser','AWSPass321',2)

    # t.t1_create_single_node_cluster('db1', 'my-cl7','single-node','dc2.large','awsuser','AWSPass321')

    # print("after create")
    # print("now waiting")
    # StopWatch.start("wait for cluster to be available")
    # redshiftclient = boto3.client('redshift')
    # waiter = redshiftclient.get_waiter('cluster_available')
    #
    # waiter.wait(
    #     ClusterIdentifier='my-cl7',
    #     WaiterConfig={
    #         'Delay': 60,
    #         'MaxAttempts': 30
    #     }
    # )
    # print("after waiting")
    # StopWatch.stop("wait for cluster to be available")

    # t.t1_create_multi_node_cluster('db1', 'my-cl2','multi-node','dc2.large','awsuser','AWSPass321',2)

    # t.t1_allow_access('my-cl7')

    #t.t1_run_select_query(host='my-cl7.ced9iqbk50ks.us-west-2.redshift.amazonaws.com')

    #t.t1_run_ddl('my-cl7',db_name='db1',host='my-cl7.ced9iqbk50ks.us-west-2.redshift.amazonaws.com',port=5439, user_name='awsuser', passwd='AWSPass321', ddl_file="./redshiftddlfile.sql")

    #t.t1_run_dml('my-cl7',db_name='db1',host='my-cl7.ced9iqbk50ks.us-west-2.redshift.amazonaws.com',port=5439, user_name='awsuser', passwd='AWSPass321', dml_file="./redshiftdmlfile.sql")

    #t.t1_run_select_query(host='my-cl7.ced9iqbk50ks.us-west-2.redshift.amazonaws.com')

    t.t1_resize_cluster_to_multi_node(cluster_id='my-cl7',node_count=2)

    StopWatch.benchmark()





