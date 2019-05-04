from cloudmesh.redshift.command.redshift import RedshiftCommand
from cloudmesh.common.run.file import run
import pytest
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.util import banner

from docopt import docopt

import sys
from contextlib import contextmanager
from io import StringIO



#
# you could have used our simple run methods from
# from cloudmehs.common.run.file.run import run
# r = run("cms redshift describe")

def execute(command):
    StopWatch.start(command)
    output = run(command)
    StopWatch.stop(command)
    return output


@pytest.mark.incremental
class TestRedshiftCommand(RedshiftCommand):
    def test_describe_all_clusters_with_no_existing(self, non_existing_cluster_id='cl111'):
        print("Describe all clusters - no existing")
        cmd_string = 'cms redshift describe ' + non_existing_cluster_id
        output = execute(cmd_string)
        assert 'Cluster not found' in output

    def test_describe_existing_cluster_existing_clusters(self):
        print("Describe all clusters, existing")
        output = execute("cms redshift describe")
        assert 'my-cl1' in output
        assert False # my-cli is not created first

    def test_describe_non_existent_cluster(self):
        print("Describe non existent")
        output = execute('cms redshift describe cl2')
        assert 'Cluster not found' in output

    def test_describe_existing_cluster(self):
        print("Describe existing")
        output = execute('cms redshift describe redshift-cluster-2')
        assert 'my-cl1' in output

    def test_delete_non_existing_cluster(self):
        print("Delete non existing")

        output = execute('cms redshift delete cl2')
        assert 'Cluster not found' in  output
        assert False

    def test_delete_existing_cluster(self):
        print("Delete existing")
        raise NotImplementedError
        # 
        #     output = execute('cms redshift delete redshift-cluster-2')
        #     assert 'final-snapshot' in  output
        assert False

    def test_change_password(self):
        print("change cluster password")
        raise NotImplementedError
        # 
        #     output = execute('cms redshift modify cl11 --newpass MyPassword321')
        #     assert 'PendingModifiedValues' in  output
        assert False

    def test_rename_cluster(self):
        print("rename cluster")
        raise NotImplementedError
        #
        #     output = execute('cms redshift modify cl11 --newid cl12')
        #     assert 'renaming' in output
        assert False

    def test_create_single_node_cluster(self):
        print("create single node cluster")
        raise NotImplementedError
        #
        #     output = execute('cms redshift create my-cl1 db1 awsuser AWSPassword321 --nodetype=dc2.large --type=single-node')
        #     assert 'creating' in output
        assert False

    def test_create_multi_node_cluster(self):
        print("create multi node cluster")
        raise NotImplementedError
        #
        #     output = execute('cms redshift create my-cl2 db1 awsuser AWSPassword321 --nodetype=dc2.large --type=multi-node --nodes=2')
        #     assert 'creating' in output
        assert False

    def test_resize_cluster_node_count(self):
        print("resizing cluster")
        raise NotImplementedError
        # 
        #     output = execute('cms redshift resize my-cl11 --type='multi-node' --nodes=2)
        #     assert 'resizing' in output
        assert False

    def test_resize_node_type(self):
        print("change node type : ")
        raise NotImplementedError
        # NOTE: Mandatory: Need to specify count of nodes, same as count of nodes in cluster
        # 
        #     output = execute('cms redshift resize my-cl21 --nodetype='ds2.xlarge' --nodes=2')
        #     assert 'resizing' in output
        assert False

    def test_benchmark(self):
        StopWatch.benchmark()
