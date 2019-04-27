from cloudmesh.redshift.Provider import Provider

import pytest


@pytest.mark.incremental
class TestRedshiftAPIProvider():
    def test_get_client(self):
        pass

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_describe_clusters(self):
        m = Provider()
        print(m.describe_clusters(args={}))

    def test_describe_cluster(self):
        m = Provider()
        print(m.describe_cluster(args={'CLUSTER_ID': 'cl2'}))

    def test_create_single_node_cluster(self):
        m = Provider()
        # print(m.create_single_node_cluster(args={'CLUSTER_ID': 'my-cl1', 'DB_NAME': 'db1', 'nodetype': 'dc2.large', 'USER_NAME': 'awsuser', 'PASSWD': 'AWSPassword321'}))
        pass

    def test_create_multi_node_cluster(self):
        m = Provider()
        # print(m.create_multi_node_cluster(args={'CLUSTER_ID': 'my-cl2', 'DB_NAME': 'db1', 'nodetype': 'dc2.large', 'USER_NAME': 'awsuser', 'PASSWD': 'AWSPassword321', 'nodes': '2'}))
        pass

    def test_delete_cluster(self):
        m = Provider()
        # m.delete_cluster(args={'CLUSTER_ID':'cl1'})
        pass

    def test_resize_cluster_node_types(self):
        m = Provider()
        # print(m.resize_cluster_node_types(args={'CLUSTER_ID':'my-cl3','nodetype':'ds2.xlarge','nodes':2}))
        pass

    def test_resize_cluster_node_count(self):
        m = Provider()
        # print(m.resize_cluster_node_count(args={'CLUSTER_ID':'cl1','type':'multi-node','nodes':3}))
        pass

    # def test_resize_cluster_to_multi_node(self):
    #     m = Provider()
    #     print(m.resize_cluster_to_multi_node(args={'CLUSTER_ID':'cl1','type':'multi-node','nodes':4}))
    #     pass

    def test_modify_cluster(self):
        m = Provider()
        print(m.modify_cluster(
            args={'CLUSTER_ID': 'cl12', 'newpass': 'AWSPassword123'}))
        # pass

    def test_rename_cluster(self):
        print("rename")
        m = Provider()
        print(m.rename_cluster(args={'CLUSTER_ID': 'cl12', 'newid': 'cl13'}))
        # pass
