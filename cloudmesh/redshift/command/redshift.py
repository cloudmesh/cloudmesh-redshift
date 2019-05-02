from __future__ import print_function
from cloudmesh.shell.command import command, map_parameters
from cloudmesh.shell.command import PluginCommand
from cloudmesh.redshift.Provider import Provider
# from cloudmesh.common import logger
# from cloudmesh.common.Printer import Printer
from docopt import docopt
# import psycopg2

class RedshiftCommand(PluginCommand):

    # def __init__(self):
    #     self.log = logger.LOGGER("redshift-manager.log")
    #     # logger.LOGGING_ON(logger.LOGGER("redshift-manager.log"))
    #     return

    # def __del__(self):
    #     # logger.LOGGING_OFF(logger.LOGGER("redshift-manager.log"))
    #     return

    def get_options(self):
        args = docopt(__doc__)
        print(args)

    # noinspection PyUnusedLocal
    @command
    def do_redshift(self, args, arguments):

        """
        ::

        Usage:
        redshift describe [CLUSTER_ID]
        redshift create CLUSTER_ID DB_NAME USER_NAME PASSWD --nodetype=NODE_TYPE [--type=TYPE] [--nodes=NODE_COUNT]
        redshift resize CLUSTER_ID [--type=TYPE] [--nodes=NODE_COUNT] [--nodetype=NODE_TYPE]
        redshift modify CLUSTER_ID [--newid=NEW_CLUSTER_ID] [--newpass=NEW_PASSWD]
        redshift delete CLUSTER_ID
        redshift allowaccess CLUSTER_ID
        redshift demoschema DB_NAME USER_NAME PASSWD HOST PORT [--createschema | --deleteschema]
        redshift runquery DB_NAME USER_NAME PASSWD HOST PORT [--empcount] [--querytext=QUERYTEXT]

        This command is used to interface with Amazon Web Services
        RedShift service to create a single-node, or multi-node cluster,
        resize, modify, and delete a database cluster

        Arguments:
            CLUSTER_ID              The AWS RedShift Cluster ID.
            DB_NAME                 The name of the database
            USER_NAME               The user name for the master user
            PASSWD                  The password of the master user
            QUERYTEXT               The text of the query to execute


        Options:
            --type=TYPE             The type of the cluster - single-node, or multi-node. [default: single-node]
            --nodetype=NODE_TYPE    The type of the clustered nodes [default: dc2.large]
            --nodes=NODE_COUNT      The number of nodes in the cluster. [default: 1]
            --newid=NEW_CLUSTER_ID  The new ID of the cluster
            --newpass=NEW_PASSWD    The new password for the master user.
            --createschema          Create the demo schema
            --deleteschema          Delete the demo schema
            --empcount              Run the count query on employees
            --querytext=QUERYTEXT        Specifies the text of the query to run

        Description:
            redshift describe CLUSTER_ID
                Gives a detailed description of the redshift cluster. If the CLUSTER_ID is not specified,
                all clusters will be listed

            redshift create CLUSTER_ID DB_NAME USER_NAME PASSWD NODE_TYPE [--type=TYPE] [--nodes=NODE_COUNT]
                Creates the redshift cluster, either single-node, or multi-node, with the given DB name, master
                username, password of the master user, with the node instance type, and count of nodes

            redshift resize CLUSTER_ID [--type=TYPE] [--nodes=NODE_COUNT]
                Resizes the cluster to the specified type, and to the count of nodes specified

            redshift modify CLUSTER_ID [--newid=NEW_CLUSTER_ID] [--newpass=NEW_PASSWD]
                Modifies the cluster by changing the cluster id or changing the password of the master user

            redshift delete CLUSTER_ID
                Delete the cluster

            Now that we have a redshift cluster, to interface with it, we need to allow access.

            redshift allowaccess CLUSTER_ID
                Configure the cluster for external (For eg. Python) access

            We can now interface with the redshift cluster.

            redshift demoschema DB_NAME USER_NAME PASSWD HOST PORT [--createschema | --deleteschema]
                Create the demo EMPLOYEE  schema

            redshift runquery DB_NAME USER_NAME PASSWD HOST PORT [--empcount | --querytext=QUERYTEXT]
                Run the canned query, or the specified SQL

        """

        map_parameters(arguments, 'type', 'nodetype', 'nodes', 'newid', 'newpass', 'createschema',
                       'deleteschema', 'empcount', 'querytext')

        redshift = Provider()

        # {'describe': False, 'CLUSTER_ID': 'cl13',
        #  'create': False, 'DB_NAME': None, 'USER_NAME': None, 'PASSWD': None, '--nodetype': 'dc1.large',
        #  '--type': 'single-node', '--nodes': '1',
        #  'resize': False, 'modify': True, '--newid': 'cl14', '--newpass': None,
        #  'delete': False,
        #  'type': 'single-node', 'nodetype': 'dc1.large', 'nodes': '1', 'newid': 'cl14', 'newpass': None}
        #
        print(arguments)
        # print(args)
        if arguments.describe:
            if arguments.get('CLUSTER_ID') is None:
                print("Blank cluster id")
                try:
                    result = redshift.describe_clusters()
                    print(result)
                finally:
                    return "Unhandled error"
            else:
                try:
                    result = redshift.describe_cluster(arguments)
                    print(result)
                finally:
                    return "Unhandled error"
        elif arguments.create:
            if arguments.get("type") == 'single-node':
                try:
                    d1 = {'CLUSTER_ID': arguments.get('CLUSTER_ID'),
                          'DB_NAME': arguments.get('DB_NAME'),
                          'nodetype': arguments.get('nodetype'),
                          'USER_NAME': arguments.get('USER_NAME'),
                          'PASSWD': arguments.get('PASSWD'),
                          'nodes': arguments.get('nodes'),
                          'CLUSTER_TYPE': arguments.get("type")}
                    result = redshift.create_single_node_cluster(d1)
                    print(result)
                finally:
                    return "Unhandled error"
            else:
                try:
                    d1 = {'CLUSTER_ID': arguments.get('CLUSTER_ID'),
                          'DB_NAME': arguments.get('DB_NAME'),
                          'nodetype': arguments.get('nodetype'),
                          'USER_NAME': arguments.get('USER_NAME'),
                          'PASSWD': arguments.get('PASSWD'),
                          'nodes': arguments.get('nodes'),
                          'CLUSTER_TYPE': arguments.get("type")}
                    result = redshift.create_multi_node_cluster(d1)
                    print(result)
                finally:
                    return "Unhandled error"
        elif arguments.resize:
            print("in resize")
            print(arguments)
            if arguments.get('nodetype') != 'dc2.large':
                # resizing nodes
                # NOTE: Necessary to have right number of nodes to be passed in
                d1 = {'CLUSTER_ID': arguments.get('CLUSTER_ID'),
                      'type': arguments.get('type'),
                      'nodetype': arguments.get('nodetype'),
                      'nodes': arguments.get('nodes')}
                # print(d1)
                result = redshift.resize_cluster_node_types(d1)
                print(result)
            elif int(arguments.get('nodes')) > 1:
                # changing type of cluster from single-node to multi-node
                d1 = {'CLUSTER_ID': arguments.get('CLUSTER_ID'),
                      'type': 'multi-node',
                      'nodetype': arguments.get('nodetype'),
                      'nodes': arguments.get('nodes')}
                # print(d1)
                result = redshift.resize_cluster_to_multi_node(d1)
                print(result)
            else:
                return "Argument error"
        elif arguments.modify:
            if arguments.get('newid') is None and arguments.get('newpass'):
                print("in modify")
                try:
                    d1 = {'CLUSTER_ID': arguments.get('CLUSTER_ID'),
                          'newpass': arguments.get('newpass')}
                    result = redshift.modify_cluster(d1)
                    print(result)
                finally:
                    return "Unhandled error"
            elif arguments.get('newid') and arguments.get('newpass') is None:
                print("in rename")
                try:
                    d1 = {'CLUSTER_ID': arguments.get('CLUSTER_ID'),
                          'newid': arguments.get('newid')}
                    result = redshift.rename_cluster(d1)
                    print(result)
                finally:
                    return "Unhandled error"
        elif arguments.delete:
            try:
                result = redshift.delete_cluster(arguments)
                print(result)
            finally:
                return "Unhandled error"
        elif arguments.allowaccess:
            try:
                result = redshift.allow_access(arguments)
                print(result)
            finally:
                return "Unhandled error"
        elif arguments.demoschema:
            print("in demoschema")
            try:
                if arguments.get('createschema'):
                    result = redshift.create_demo_schema(arguments)
                elif arguments.get('deleteschema'):
                    result = redshift.delete_demo_schema(arguments)
                print(result)
            finally:
                return "Unhandled error"
        elif arguments.runquery:
            print("In run query")
            try:
                if arguments.get('empcount'):
                    print("in empcount")
                    arguments['querytext'] = 'SELECT COUNT(*) FROM emp;'
                    result = redshift.runselectquery_text(arguments)
                elif arguments.get('querytext'):
                    print("in querytext")
                    result = redshift.runselectquery_text(arguments)
                print(result)
            finally:
                return "Unhandled error"

        else:
            print(self.get_options())


if __name__ == "__main__":
    print("In redshift.py")
