from cloudmesh.redshift.command.redshift import RedshiftCommand

import pytest

from cloudmesh.common.util import banner

from docopt import docopt


import sys
from contextlib import contextmanager
from io import StringIO


doc = RedshiftCommand.__doc__


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


@pytest.mark.incremental
class TestRedshiftCommand(RedshiftCommand):
    def test_describe_all_clusters_with_no_existing(self):
        sys.stdout.write("Describe all clusters - no existing")
        r = RedshiftCommand()
        # args = docopt(doc, ["describe", "cl1"])
        with captured_output() as (out, err):
            sys.stdout.write(r.do_redshift('describe'))
            output = out.getvalue().strip()
            assert 'Cluster not found' in  output
        # pass

    def test_describe_existing_cluster_existing_clusters(self):
        sys.stdout.write("Describe all clusters, existing")
        r = RedshiftCommand()
        with captured_output() as (out, err):
            sys.stdout.write(r.do_redshift('describe'))
            output = out.getvalue().strip()
            assert 'redshift-cluster-2' in  output
        # pass

    def test_describe_non_existent_cluster(self):
        print("Describe non existent")
        r = RedshiftCommand()
        # args = docopt(doc, ["describe", "cl1"])
        with captured_output() as (out, err):
            print(r.do_redshift('describe cl2'))
            output = out.getvalue().strip()
            assert 'Cluster not found' in  output
        # pass

    def test_describe_existing_cluster(self):
        print("Describe existing")
        r = RedshiftCommand()
        with captured_output() as (out, err):
            print(r.do_redshift('describe redshift-cluster-2'))
            output = out.getvalue().strip()
            assert 'redshift-cluster-2' in  output
        # pass

    def test_delete_non_existing_cluster(self):
        print("Delete non existing")
        # r = RedshiftCommand()
        # with captured_output() as (out, err):
        #     print(r.do_redshift('delete cl2'))
        #     output = out.getvalue().strip()
        #     assert 'Cluster not found' in  output
        pass

    def test_delete_existing_cluster(self):
        print("Delete existing")
        # r = RedshiftCommand()
        # with captured_output() as (out, err):
        #     print(r.do_redshift('delete redshift-cluster-2'))
        #     output = out.getvalue().strip()
        #     assert 'final-snapshot' in  output
        pass

    def test_change_password(self):
        print("change cluster password")
        # r = RedshiftCommand()
        # with captured_output() as (out, err):
        #     print(r.do_redshift('modify cl11 --newpass MyPassword321'))
        #     output = out.getvalue().strip()
        #     assert 'PendingModifiedValues' in  output
        pass

    def test_rename_cluster(self):
        print("rename cluster")
        # r = RedshiftCommand()
        # with captured_output() as (out, err):
        #     print(r.do_redshift('modify cl11 --newid cl12'))
        #     output = out.getvalue().strip()
        #     assert 'renaming' in output
        pass

    def test_create_single_node_cluster(self):
        print("create single node cluster")
        # r = RedshiftCommand()
        # with captured_output() as (out, err):
        #     print(r.do_redshift('create my-cl1 db1 awsuser AWSPassword321 --nodetype=dc2.large --type=single-node'))
        #     output = out.getvalue().strip()
        #     assert 'creating' in output
        pass

    def test_create_multi_node_cluster(self):
        print("create multi node cluster")
        # r = RedshiftCommand()
        # with captured_output() as (out, err):
        #     print(r.do_redshift('create my-cl2 db1 awsuser AWSPassword321 --nodetype=dc2.large --type=multi-node --nodes=2'))
        #     output = out.getvalue().strip()
        #     assert 'creating' in output
        pass

    def test_resize_cluster_node_count(self):
        print("resizing cluster")
        # r = RedshiftCommand()
        # with captured_output() as (out, err):
        #     print(r.do_redshift('resize my-cl11 --type='multi-node' --nodes=2))
        #     output = out.getvalue().strip()
        #     assert 'resizing' in output
        pass

    def test_resize_node_type(self):
        print("change node type : ")
        # NOTE: Mandatory: Need to specify count of nodes, same as count of nodes in cluster
        # r = RedshiftCommand()
        # with captured_output() as (out, err):
        #     print(r.do_redshift('resize my-cl21 --nodetype='ds2.xlarge' --nodes=2'))
        #     output = out.getvalue().strip()
        #     assert 'resizing' in output
        pass