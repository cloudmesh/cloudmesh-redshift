from cloudmesh.redshift.api.manager import Manager

import pytest


@pytest.mark.incremental
class TestRedshiftAPIManager():

    # def __new__(Manager):
    #     print("new called")
    #     o = object.__new__(Manager)
    #     print(m.describe_cluster('redshift-cluster-1'))
    #     pass

    def test_get_client(self):
        pass

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_describe_clusters(self):
        m = Manager()
        print(m.describe_clusters(args={}))
        pass

    def test_describe_cluster(self):
        m = Manager()
        print(m.describe_cluster(args={'CLUSTER_ID':'cl2'}))
        pass

    def test_create_single_node_cluster(self):
        m = Manager()
        # print(m.create_single_node_cluster(args={'DB_NAME':'mydb1','CLUSTER_ID':'cl1',
        #                                                'NODE_TYPE':'dc2.large','USERNAME':'awsuser','PASSWD':'AWSPass321'}))

        pass

    def test_create_multi_node_cluster(self):
        m = Manager()
        # print(m.create_multi_node_cluster(args={'DB_NAME':'mydb1','CLUSTER_ID':'cl3', 'NODE_TYPE':'dc2.large',
        #                                         'USERNAME':'awsuser','PASSWD':'AWSPass321','NODE_NUM':3}))

        pass

    def test_delete_cluster(self):
        m = Manager()
        # m.delete_cluster(args={'CLUSTER_ID':'cl1'})
        pass

    # def test_resize_cluster_node_types(self):
    #     m = Manager()
    #     # print(m.resize_cluster_node_types(args={'CLUSTER_ID':'cl4','NODE_TYPE':'dc2.8xlarge','NODE_NUM':3}))
    #     pass

    # def test_resize_cluster_nodes(self):
    #     m = Manager()
    #     print(m.resize_cluster_nodes(args={'CLUSTER_ID':'cl1','CLUSTER_TYPE':'multi-node','NODE_NUM':1}))
    #     pass


    # def test_resize_cluster_to_multi_node(self):
    #     m = Manager()
    #     print(m.resize_cluster_to_multi_node(args={'CLUSTER_ID':'cl1','CLUSTER_TYPE':'multi-node','NODE_NUM':4}))
    #     pass


    def test_modify_cluster(self):
        m = Manager()
        # print(m.modify_cluster(args={'CLUSTER_ID':'cl3','PASSWD':'AWSPassword321'))
        pass

    def test_rename_cluster(self):
        m = Manager()
        # print(m.rename_cluster(args={'CLUSTER_ID':'cl3','NEW_CLUSTER_ID':'cl4'}))
        pass
