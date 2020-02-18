###############################################################
# pytest -v --capture=no tests/test_redshift_cmd.py
# pytest -v  tests/test_redshift_cmd.py
# pytest -v --capture=no -v --nocapture tests/test_redshift_manager..py::TestRedshiftCommand::<METHODNAME>
###############################################################

from cloudmesh.redshift.command.redshift import RedshiftCommand
from cloudmesh.common.run.file import run
import pytest
from cloudmesh.common.StopWatch import StopWatch
# from cloudmesh.common.util import banner
#
# from docopt import docopt
#
# import sys
# from contextlib import contextmanager
# from io import StringIO

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
    def t1_describe_all_clusters_with_no_existing(self, cluster_id='cl111'):
        print("Describe all clusters - no existing")
        cmd_string = 'cms redshift describe ' + cluster_id
        output = execute(cmd_string)
        print(output)
        assert 'Cluster not found' in output

    def t1_describe_existing_cluster_existing_clusters(self):
        print("Describe all clusters, existing")
        output = execute("cms redshift describe")
        print(output)
        assert 'ClusterIdentifier' in output
        # assert False # my-cli is not created first

    def t1_describe_non_existent_cluster(self, cluster_id='my-cl1111'):
        print("Describe non existent")
        cmd_str = "cms redshift describe " + cluster_id
        output = execute(cmd_str)
        print(output)
        assert 'Cluster Not Found' in output

    def t1_describe_existing_cluster(self, cluster_id='my-cl1'):
        print("Describe existing")
        cmd_str = "cms redshift describe " + cluster_id
        output = execute(cmd_str)
        print(output)
        assert cluster_id in output

    def t1_create_single_node_cluster(self, db_name='db1', cluster_id='my-cl1', cluster_type='single-node',
                                      node_type='dc2.large', user_name='awsuser', passwd='AWSPass321'):
        print("Create single node cluster")
        cmd_string = "cms redshift create " + cluster_id + " " + db_name + " " + user_name + " " \
                     + passwd + " --nodetype=" + node_type+ " --type=" + cluster_type
        print(cmd_string)
        output = execute(cmd_string)
        print(output)
        assert 'creating' in output

    def t1_create_multi_node_cluster(self, db_name='db1', cluster_id='my-cl1', cluster_type='single-node',
                                      node_type='dc2.large', user_name='awsuser', passwd='AWSPass321', node_count=2):
        print("Create multi-node cluster")
        cmd_string = "cms redshift create " + cluster_id + " " + db_name + " " + user_name + " " \
                     + passwd + " --nodetype=" + node_type + " --type=" + cluster_type + " --nodes=" + str(node_count)
        print(cmd_string)
        output = execute(cmd_string)
        print(output)
        assert 'creating' in output

    def t1_delete_non_existing_cluster(self, cluster_id):
        print("Delete non existing")
        cmd_string = "cms redshift delete " + cluster_id
        output = execute(cmd_string)
        print(output)
        assert 'Cluster not found' in  output

    def t1_delete_existing_cluster(self, cluster_id):
        print("Delete existing")
        cmd_string = "cms redshift delete " + cluster_id
        output = execute(cmd_string)
        print(output)
        assert 'final-snapshot' in  output

    def t1_change_password(self, cluster_id='my-cl1', new_pass='MyNewPass321'):
        print("change cluster password")
        cmd_string = "cms redshift modify " + cluster_id + " --newpass " + new_pass
        print(cmd_string)
        output = execute(cmd_string)
        print(output)
        assert 'PendingModifiedValues' in  output

    def t1_rename_cluster(self, cluster_id='my-cl1', new_id='my-cl111'):
        print("rename cluster")
        cmd_string = "cms redshift modify " + cluster_id + " --newid " + new_id
        print(cmd_string)
        output = execute(cmd_string)
        print(output)
        assert 'Renaming' in output

    def t1_resize_cluster_node_count(self, cluster_id='my-cl1', cluster_type='multi-node', node_count=2):
        print("resizing cluster")
        cmd_string = "cms redshift resize " + cluster_id + " --type= " + cluster_type + " --nodes= " + str(node_count)
        print(cmd_string)
        output = execute(cmd_string)
        print(output)
        assert 'Resizing' in output

    def t1_resize_node_type(self, cluster_id='my-cl1', node_type='ds2.xlarge', node_count=2):
        print("change node type : ")
    # NOTE: Mandatory: Need to specify count of nodes, same as count of nodes in cluster
        cmd_string = "cms redshift resize " + cluster_id + " --nodetype=" + node_type + " --nodes=" + str(node_count)
        print(cmd_string)
        output = execute(cmd_string)
        print(output)
        assert 'Resizing' in output

    def t1_allow_access(self, cluster_id='my-cl1'):
        print("allow access")
        cmd_string = "cms redshift allowaccess " + cluster_id
        output = execute(cmd_string)
        print(output)
        assert 'Allowing access' in output

    def t1_runddl(self, db_name='db1', user_name='awsuser', passwd='AWSPass321',
                  host='my-cl7.ced9iqbk50ks.us-west-2.redshift.amazonaws.com', port=5439,
                  ddlfile='./redshiftddlfile.sql'):
        print("Run DDL")
        cmd_string = "cms redshift runddl " + db_name + " " + user_name + " " + passwd + " " + host + " " + str(port) \
                     + " --ddlfile=" + ddlfile
        print(cmd_string)
        output = execute(cmd_string)
        print(output)
        assert 'Unable to connect' not in output

    def t1_rundml(self, db_name='db1', user_name='awsuser', passwd='AWSPass321',
                  host='my-cl7.ced9iqbk50ks.us-west-2.redshift.amazonaws.com', port=5439,
                  dmlfile='./redshiftdmlfile.sql'):
        print("Run DML")
        cmd_string = "cms redshift rundml " + db_name + " " + user_name + " " + passwd + " " + host + " " + str(port) \
                     + " --dmlfile=" + dmlfile
        print(cmd_string)
        output = execute(cmd_string)
        print(output)
        assert 'Unable to connect' not in output

    def t1_runquery(self, db_name='db1', user_name='awsuser', passwd='AWSPass321',
                  host='my-cl7.ced9iqbk50ks.us-west-2.redshift.amazonaws.com', port=5439,
                  query_text='SELECT COUNT(*) FROM EMP'):
        print("Run Query")
        cmd_string = "cms redshift rundml " + db_name + " " + user_name + " " + passwd + " " + host + " " + str(port) \
                     + " --querytext='" + query_text + "'"
        print(cmd_string)
        output = execute(cmd_string)
        print(output)
        assert 'Allowing access' in output


    def test_benchmark(self):

        #The sequence of execution is very important
        # Most redshift commands take upwards of 2 minutes for each operation


        # Initially you can describe the clusters (when no clusters exist)

        # Then run a

        # t.t1_describe_all_clusters_with_no_existing()
        # t.t1_describe_existing_cluster_existing_clusters()
        # t.t1_describe_existing_cluster('cl8')
        # t.t1_describe_non_existent_cluster('cl9')
        # t.t1_allow_access('cl8')

        # t.t1_create_single_node_cluster('db1','my-cl1','single-node','dc2.large','awsuser','AWSPass321')

        # t.t1_create_multi_node_cluster('db1','my-cl2','multi-node','dc2.large','awsuser','AWSPass321',2)
        # t.t1_runddl('db1','awsuser','AWSPass321','cl8.ced9iqbk50ks.us-west-2.redshift.amazonaws.com',5439,
        #            './redshiftddlfile.sql')

        # t.t1_rundml('db1','awsuser','AWSPass321','cl8.ced9iqbk50ks.us-west-2.redshift.amazonaws.com',5439,
        #           './redshiftdmlfile.sql')

        # t.t1_rename_cluster('cl8','cl9')

        t.t1_change_password('cl9', 'MyNewPass321')

        StopWatch.benchmark()

if __name__ == "__main__":
    print("In test_redshift_cmd")
    t = TestRedshiftCommand()
    # t.t1_describe_all_clusters_with_no_existing()
    #t.t1_describe_existing_cluster_existing_clusters()
    #t.t1_describe_existing_cluster('cl8')
    #t.t1_describe_non_existent_cluster('cl9')
    #t.t1_allow_access('cl8')

    #t.t1_create_single_node_cluster('db1','my-cl1','single-node','dc2.large','awsuser','AWSPass321')

    #t.t1_create_multi_node_cluster('db1','my-cl2','multi-node','dc2.large','awsuser','AWSPass321',2)
    #t.t1_runddl('db1','awsuser','AWSPass321','cl8.ced9iqbk50ks.us-west-2.redshift.amazonaws.com',5439,
    #            './redshiftddlfile.sql')

    #t.t1_rundml('db1','awsuser','AWSPass321','cl8.ced9iqbk50ks.us-west-2.redshift.amazonaws.com',5439,
    #           './redshiftdmlfile.sql')

    #t.t1_rename_cluster('cl8','cl9')

    t.t1_change_password('cl9','MyNewPass321')
    StopWatch.benchmark()
