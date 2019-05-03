from __future__ import print_function
from cloudmesh.shell.command import command, map_parameters
from cloudmesh.shell.command import PluginCommand
from cloudmesh.redshift.Provider import Provider
# from cloudmesh.common import logger
# from cloudmesh.common.Printer import Printer
from docopt import docopt
# import psycopg2
import base64

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
        redshift runddl DB_NAME USER_NAME PASSWD HOST PORT --ddlfile=FILE_NAME
        redshift rundml DB_NAME USER_NAME PASSWD HOST PORT --dmlfile=FILE_NAME
        redshift runquery DB_NAME USER_NAME PASSWD HOST PORT [--empcount] [--querytext=QUERY_TEXT]

        This command is used to interface with Amazon Web Services
        RedShift service to create a single-node, or multi-node cluster,
        resize, modify, and delete a database cluster

        Arguments:
            CLUSTER_ID              The AWS RedShift Cluster ID.
            DB_NAME                 The name of the database
            USER_NAME               The user name for the master user
            PASSWD                  The password of the master user
            QUERY_TEXT               The text of the query to execute
            FILE_NAME               The file containing the queries

        Options:
            --type=TYPE             The type of the cluster - single-node, or multi-node. [default: single-node]
            --nodetype=NODE_TYPE    The type of the clustered nodes [default: dc2.large]
            --nodes=NODE_COUNT      The number of nodes in the cluster. [default: 1]
            --newid=NEW_CLUSTER_ID  The new ID of the cluster
            --newpass=NEW_PASSWD    The new password for the master user.
            --createschema          Create the demo schema
            --deleteschema          Delete the demo schema
            --ddlfile=FILE_NAME     Specify the DDL (CREATE TABLE, ALTER TABLE, DROP TABLE) to run in the file
            --dmlfile=FILE_NAME     Specify the DML statements (INSERT, UPDATE, DELETE) to run in the file
            --empcount              Run the count query on employees (demo schema only)
            --querytext=QUERY_TEXT   Specifies the text of the query to run

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

            redshift runddl DB_NAME USER_NAME PASSWD HOST PORT --ddlfile=FILE_NAME
                Run the DDL statements (CREATE TABLE, ALTER TABLE, DROP TABLE) specified in the file

            redshift rundml DB_NAME USER_NAME PASSWD HOST PORT --dmlfile=FILE_NAME
                Run the DML statements (INSERT, UPDATE, DELETE) specified in the file

            redshift runquery DB_NAME USER_NAME PASSWD HOST PORT [--empcount] [--querytext=QUERY_TEXT]
                Run the canned query, or the specified SQL

        """

        map_parameters(arguments, 'type', 'nodetype', 'nodes', 'newid', 'newpass', 'createschema',
                       'deleteschema', 'empcount', 'querytext', 'ddlfile',
                       'dmlfile')

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
            cluster_id = arguments.get('CLUSTER_ID')
            if cluster_id is None:
                print("Blank cluster id")
                try:
                    result = redshift.describe_clusters()
                    print(result)
                finally:
                    return "Unhandled error"
            else:
                try:
                    result = redshift.describe_cluster(cluster_id)
                    print(result)
                finally:
                    return "Unhandled error"
        elif arguments.create:
            if arguments.get("type") == 'single-node':

                try:
                    db_name = arguments.get('DB_NAME')
                    cluster_id = arguments.get('CLUSTER_ID')
                    cluster_type = arguments.get("type")
                    node_type = arguments.get('nodetype')
                    user_name = arguments.get('USER_NAME')
                    passwd = arguments.get('PASSWD')
                    node_count = int(arguments.get('nodes'))
                    result = redshift.create_single_node_cluster(db_name, cluster_id, cluster_type, node_type, user_name, passwd)
                    print(result)
                finally:
                    return "Unhandled error"
            else:
                try:
                    db_name = arguments.get('DB_NAME')
                    cluster_id = arguments.get('CLUSTER_ID')
                    cluster_type = arguments.get("type")
                    node_type = arguments.get('nodetype')
                    user_name = arguments.get('USER_NAME')
                    passwd = arguments.get('PASSWD')
                    node_count = int(arguments.get('nodes'))
                    result = redshift.create_multi_node_cluster(db_name, cluster_id, cluster_type, node_type, user_name, passwd, node_count)
                    print(result)
                finally:
                    return "Unhandled error"
        elif arguments.resize:
            print("in resize")
            print(arguments)
            node_type = arguments.get('nodetype')
            cluster_id = arguments.get('CLUSTER_ID')
            cluster_type = arguments.get("type")
            node_count = int(arguments.get('nodes'))
            if node_type != 'dc2.large':
                # resizing nodes
                # NOTE: Necessary to have right number of nodes to be passed in
                result = redshift.resize_cluster_node_types(cluster_id, cluster_type, node_count)
                print(result)
            elif node_count > 1:
                # changing type of cluster from single-node to multi-node
                cluster_type = 'multi-node'
                # print(d1)
                result = redshift.resize_cluster_to_multi_node(cluster_id, cluster_type, node_count, node_type)
                print(result)
            else:
                return "Argument error"
        elif arguments.modify:
            new_id = arguments.get('newid')
            new_pass = arguments.get('newpass')
            cluster_id = arguments.get('CLUSTER_ID')

            if new_id is None and new_pass:
                print("in modify")
                try:
                    result = redshift.modify_cluster(cluster_id, new_pass)
                    print(result)
                finally:
                    return "Unhandled error"
            elif new_id and new_pass is None:
                print("in rename")
                try:
                    result = redshift.rename_cluster(cluster_id, new_id)
                    print(result)
                finally:
                    return "Unhandled error"
        elif arguments.delete:
            cluster_id = arguments.get('CLUSTER_ID')
            try:
                result = redshift.delete_cluster(cluster_id)
                print(result)
            finally:
                return "Unhandled error"
        elif arguments.allowaccess:
            cluster_id = arguments.get('CLUSTER_ID')
            try:
                result = redshift.allow_access(cluster_id)
                print(result)
            finally:
                return "Unhandled error"
        elif arguments.demoschema:

            db_name = arguments.get('DB_NAME')
            user_name = arguments.get('USER_NAME')
            passwd = arguments.get('PASSWD')

            host = arguments.get('HOST')
            port = arguments.get('PORT')
            if port is None:
                port = 5439

            host_list = host.split('.')
            cluster_id = host_list[0]
            print("in demoschema")
            try:
                if arguments.get('createschema'):
                    result = redshift.create_demo_schema(cluster_id, db_name, host, port, user_name, passwd)
                elif arguments.get('deleteschema'):
                    result = redshift.delete_demo_schema(cluster_id, db_name, host, port, user_name, passwd)
                print(result)
            finally:
                return "Unhandled error"
        elif arguments.runddl:
            print("In run DDL")

            db_name = arguments.get('DB_NAME')
            user_name = arguments.get('USER_NAME')
            passwd = arguments.get('PASSWD')

            host = arguments.get('HOST')
            port = arguments.get('PORT')
            if port is None:
                port = 5439
            ddl_file_name = arguments.get('ddlfile')

            fd = open(ddl_file_name, 'r')
            sql_file_contents = fd.read()
            fd.close()
            b64_sql_file_contents = base64.b64encode(bytes(sql_file_contents, 'ascii'))

            host_list = host.split('.')
            cluster_id = host_list[0]
            try:
                print("in run ddl")
                result = redshift.runddl(cluster_id, db_name, host, port, user_name, passwd, b64_sql_file_contents)
            finally:
                return "Unhandled error"

        elif arguments.rundml:
            print("In run DML")

            db_name = arguments.get('DB_NAME')
            user_name = arguments.get('USER_NAME')
            passwd = arguments.get('PASSWD')

            host = arguments.get('HOST')
            port = arguments.get('PORT')
            if port is None:
                port = 5439
            dml_file_name = arguments.get('dmlfile')

            fd = open(dml_file_name, 'r')
            sql_file_contents = fd.read()
            fd.close()
            b64_sql_file_contents = base64.b64encode(bytes(sql_file_contents,'utf-8'))

            host_list = host.split('.')
            cluster_id = host_list[0]
            try:
                print("in run dml")
                result = redshift.rundml(cluster_id, db_name, host, port, user_name, passwd, b64_sql_file_contents)
            finally:
                return "Unhandled error"
        elif arguments.runquery:
            print("In run query")

            db_name = arguments.get('DB_NAME')
            user_name = arguments.get('USER_NAME')
            passwd = arguments.get('PASSWD')

            host = arguments.get('HOST')
            port = arguments.get('PORT')
            if port is None:
                port = 5439
            emp_count = arguments.get('empcount')
            query_text = arguments.get('querytext')
            host_list = host.split('.')
            cluster_id = host_list[0]

            print(query_text)
            try:
                if emp_count:
                    print("in empcount")
                    query_text = 'SELECT COUNT(*) FROM emp;'
                    result = redshift.runselectquery_text(cluster_id, db_name, host, port, user_name, passwd, query_text)
                elif query_text:
                    print("in querytext")
                    result = redshift.runselectquery_text(cluster_id, db_name, host, port, user_name, passwd, query_text)
                    print(result)
                else:
                    print("error in options")
            finally:
                return "Unhandled error"

        else:
            print(self.get_options())


if __name__ == "__main__":
    print("In redshift.py")
