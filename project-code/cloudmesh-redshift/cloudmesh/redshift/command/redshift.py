from __future__ import print_function
from cloudmesh.shell.command import command, map_parameters
from cloudmesh.shell.command import PluginCommand
from cloudmesh.redshift.api.manager import Manager
from cloudmesh.common import logger
from cloudmesh.common.Printer import Printer
import sys

class RedshiftCommand(PluginCommand):

    def __init__(self):
        self.log = logger.LOGGER("redshift-manager.log")
        # logger.LOGGING_ON(logger.LOGGER("redshift-manager.log"))
        return

    def __del__(self):
        # logger.LOGGING_OFF(logger.LOGGER("redshift-manager.log"))
        return

    # noinspection PyUnusedLocal
    @command
    def do_redshift(self, args, arguments):

        """
        ::

        Usage:
        redshift describe CLUSTER_ID
        redshift create CLUSTER_ID DB_NAME USER_NAME PASSWD NODE_TYPE [--type=TYPE] [--nodes=NODE_COUNT]
        redshift resize CLUSTER_ID [--type=TYPE] [--nodes=NODE_COUNT]
        redshift modify CLUSTER_ID [--newid=NEW_CLUSTER_ID] [--newpass=NEW_PASSWD]
        redshift delete CLUSTER_ID

        This command is used to interface with Amazon Web Services
        RedShift service to create a single-node, or multi-node cluster,
        resize, modify, and delete a database cluster

        Arguments:
            CLUSTER_ID              The AWS RedShift Cluster ID.
            DB_NAME                 The name of the database
            USER_NAME               The user name for the master user
            PASSWD                  The password of the master user
            NODE_TYPE               The type of the clustered nodes [default: dc1.large]

        Options:
            --type=TYPE             The type of the cluster - single-node, or multi-node. [default: single-node]
            --nodetype=NODE_TYPE    The type of the clustered nodes [default: dc1.large]
            --nodes=NODE_COUNT      The number of nodes in the cluster. [default: 1]
            --newid=NEW_CLUSTER_ID  The new ID of the cluster
            --newpass=NEW_PASSWD    The new password for the master user.


        Description:
            redshift describe CLUSTER_ID
                Gives a detailed description of the redshift cluster

            redshift create CLUSTER_ID DB_NAME USER_NAME PASSWD NODE_TYPE [--type=TYPE] [--nodes=NODE_COUNT]
                Creates the redshift cluster, either single-node, or multi-node, with the given DB name, master
                username, password of the master user, with the node instance type, and count of nodes

            redshift resize CLUSTER_ID [--type=TYPE] [--nodes=NODE_COUNT]
                Resizes the cluster to the specified type, and to the count of nodes specified

            redshift modify CLUSTER_ID [--newid=NEW_CLUSTER_ID] [--newpass=NEW_PASSWD]
                Modifies the cluster by changing the cluster id or changing the password of the master user

            redshift delete CLUSTER_ID
                Delete the cluster

        """

        # map_parameters(arguments, 'status', 'format', 'type', 'master', 'node', 'count', 'state')
        # print(arguments)

        redshift = Manager()

        # self.log.info('Arguments are : ', arguments, ' Length : ', len(arguments))
        # sys.stderr.write('Arguments are : ', arguments, ' Length : ', len(arguments))
        # sys.stdout.write(Printer.dict(arguments))

        if arguments.describe:
            # redshift
            # describe  CLUSTER_ID

            if args.get('CLUSTER_ID') is None:
                # if arguments. == 0:
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

        elif arguments['create']:
            # redshift
            # create  CLUSTER_ID   DB_NAME   USER_NAME   PASSWD   NODE_TYPE  [--type = TYPE] [--nodes = NODE_COUNT]

            try:
                result = redshift.create_single_node_cluster()
                print(result)
            finally:
                return "Unhandled error"

            pass
        elif arguments['resize']:
            # redshift
            # resize  CLUSTER_ID  [--type = TYPE] [--nodes = NODE_COUNT]
            pass
        elif arguments['modify']:
            # redshift
            # modify  CLUSTER_ID  [--newid = NEW_CLUSTER_ID] [--newpass = NEW_PASSWD]
            pass
        elif arguments['delete']:
            # redshift
            # delete  CLUSTER_ID
            pass

