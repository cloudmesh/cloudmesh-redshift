from cloudmesh.redshift.Provider import Provider
from cloudmesh.common.StopWatch import StopWatch
import pytest



@pytest.mark.incremental
class TestRedshiftAPIProvider():
    def test_get_client(self):
        pass

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_describe_clusters(self):
        StopWatch.start("Provider")
        m = Provider()
        StopWatch.stop("Provider")
        print(m.describe_clusters(args={}))

    def test_describe_cluster(self):
        StopWatch.start("describe cluster")
        m = Provider()
<<<<<<< HEAD:cloudmesh/tests/apitests/test_manager.py
        print(m.describe_cluster(args={'CLUSTER_ID': 'my-cl1'}))
=======
        StopWatch.stop("describe cluster")
        print(m.describe_cluster(args={'CLUSTER_ID': 'cl2'}))
        # no assertion
        assert False
>>>>>>> 400567e5b6971378a1ecd5ac7975c59d5c6339b1:tests/test_redshift_manager.py

    def test_create_single_node_cluster(self):
        m = Provider()
        raise NotImplementedError
        # print(m.create_single_node_cluster(args={'CLUSTER_ID': 'my-cl1', 'DB_NAME': 'db1', 'nodetype': 'dc2.large', 'USER_NAME': 'awsuser', 'PASSWD': 'AWSPassword321'}))
        assert False

    def test_create_multi_node_cluster(self):
        m = Provider()
        raise NotImplementedError
        # print(m.create_multi_node_cluster(args={'CLUSTER_ID': 'my-cl2', 'DB_NAME': 'db1', 'nodetype': 'dc2.large', 'USER_NAME': 'awsuser', 'PASSWD': 'AWSPassword321', 'nodes': '2'}))
        assert False

    def test_delete_cluster(self):
        m = Provider()
        raise NotImplementedError
        # m.delete_cluster(args={'CLUSTER_ID':'cl1'})
        assert False

    def test_resize_cluster_node_types(self):
        m = Provider()
        raise NotImplementedError
        # print(m.resize_cluster_node_types(args={'CLUSTER_ID':'my-cl3','nodetype':'ds2.xlarge','nodes':2}))
        assert False

    def test_resize_cluster_node_count(self):
        m = Provider()
        raise NotImplementedError
        # print(m.resize_cluster_node_count(args={'CLUSTER_ID':'cl1','type':'multi-node','nodes':3}))
        assert False

    # def test_resize_cluster_to_multi_node(self):
    #     m = Provider()
    #     print(m.resize_cluster_to_multi_node(args={'CLUSTER_ID':'cl1','type':'multi-node','nodes':4}))
    #     assert False

    def test_modify_cluster(self):
        m = Provider()
<<<<<<< HEAD:cloudmesh/tests/apitests/test_manager.py
        # print(m.modify_cluster(
        #     args={'CLUSTER_ID': 'cl12', 'newpass': 'AWSPassword123'}))
        pass
=======
        print(m.modify_cluster(
            args={'CLUSTER_ID': 'cl12', 'newpass': 'AWSPassword123'}))
        # pass
        raise NotImplementedError
        # no assertion
        assert false
>>>>>>> 400567e5b6971378a1ecd5ac7975c59d5c6339b1:tests/test_redshift_manager.py

    def test_rename_cluster(self):
        print("rename")
        # m = Provider()
        # print(m.rename_cluster(args={'CLUSTER_ID': 'cl12', 'newid': 'cl13'}))
        pass

    def test_mongo(self):
        print("In Mongo")
        m = Provider()
<<<<<<< HEAD:cloudmesh/tests/apitests/test_manager.py
        m.update_dict()
        pass

if __name__ == "__main__":
    print("In test_manager")

=======
        print(m.rename_cluster(args={'CLUSTER_ID': 'cl12', 'newid': 'cl13'}))
        # pass
        # no assertion
        assert False

    def test_benchmark(self):
        StopWatch.benchmark()
>>>>>>> 400567e5b6971378a1ecd5ac7975c59d5c6339b1:tests/test_redshift_manager.py