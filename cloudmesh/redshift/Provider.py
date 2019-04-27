from cloudmesh.management.configuration.config import Config
import uuid
import boto3
from botocore.exceptions import ClientError
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate


class Provider(object):

    def __init__(self, service="redshift"):
        VERBOSE("initialize redshift manager")
        self.key_id = None
        self.access_key = None
        self.region = None
        self.config = Config()

        self.key_id = self.config[
            'cloudmesh.cloud.aws.credentials.EC2_ACCESS_ID']
        self.access_key = self.config[
            'cloudmesh.cloud.aws.credentials.EC2_SECRET_KEY']
        self.region = self.config['cloudmesh.cloud.aws.credentials.region']

        self.client = boto3.client(
            service,
            region_name=self.region,
            aws_access_key_id=self.key_id,
            aws_secret_access_key=self.access_key)

    # def parse_options(self, options, states):
    #     result = []
    #
    #     if 'all' not in options:
    #         for option in options:
    #             if option in states:
    #                 result += [states[option]]
    #     return result

    def update_dict(self, d):
        d["cm"] = {
            "kind": "redshift",
            "name": "redshift",
            "cloud": "aws",
        }
        return d

    def update_status(self, results=None, name=None, status=None):
        return self.update_dict(
            {"cloud": "aws",
             "kind": "redshift",
             "cluster": results,
             "name": name,
             "status": status})

    #
    # BUG: all dicts that go in teh db must be updated woth update_dict
    #      afterthat the @DatabaseUpdate will work

    # @DatabaseUpdate()
    def describe_clusters(self, args):
        try:
            results = self.client.describe_clusters()
            return results['Clusters']
        except ClientError as e:
            if e.response['Error']['Code'] == 'ClusterNotFound':
                return "Cluster not found"
            else:
                return "Unexpected error: %s" % e

    #
    # BUG: all dicts that go in teh db must be updated woth update_dict
    #      afterthat the @DatabaseUpdate will work

    # @DatabaseUpdate()
    def describe_cluster(self, args):
        try:
            results = self.client.describe_clusters(
                ClusterIdentifier=args['CLUSTER_ID'])
            return results['Clusters']
        # except client.exceptions.ClusterNotFoundException as e:
        #     print("Cluster not found")
        #     return e
        # except client.exceptions.ServiceNotFoundException as e:
        #     print("Service not found")
        #     return e
        # finally:
        #     return "Unhandled error"
        except ClientError as e:
            if e.response['Error']['Code'] == 'ClusterNotFound':
                return "Cluster not found"
            else:
                return "Unexpected error: %s" % e

    #
    # BUG: all dicts that go in teh db must be updated woth update_dict
    #      afterthat the @DatabaseUpdate will work

    @DatabaseUpdate()
    def create_single_node_cluster(self, args):
        if args.get('CLUSTER_TYPE') is not None:
            cluster_type = args['CLUSTER_TYPE']
        else:
            cluster_type = 'single-node'

        results = self.client.create_cluster(
            DBName=args['DB_NAME'],
            ClusterIdentifier=args['CLUSTER_ID'],
            ClusterType=cluster_type,
            NodeType=args['nodetype'],
            MasterUsername=args['USER_NAME'],
            MasterUserPassword=args['PASSWD'],
            Port=5439,
            AllowVersionUpgrade=True,
            # NumberOfNodes=1, # needs to be supplied if ClusterType is multi-node
            PubliclyAccessible=True,
            Encrypted=False
        )

        return self.update_status(results=results,
                                  name=args['CLUSTER_ID'],
                                  status="Creating")

    @DatabaseUpdate()
    def create_multi_node_cluster(self, args):

        if args.get('CLUSTER_TYPE') is not None:
            cluster_type = args['CLUSTER_TYPE']
        else:
            cluster_type = 'multi-node'

        results = self.client.create_cluster(
            DBName=args['DB_NAME'],
            ClusterIdentifier=args['CLUSTER_ID'],
            ClusterType=cluster_type,
            NodeType=args['nodetype'],
            MasterUsername=args['USER_NAME'],
            MasterUserPassword=args['PASSWD'],
            Port=5439,
            AllowVersionUpgrade=True,
            NumberOfNodes=int(args['nodes']),
            PubliclyAccessible=True,
            Encrypted=False
        )
        return self.update_status(results=results,
                                  name=args['CLUSTER_ID'],
                                  status="Creating")

    @DatabaseUpdate()
    def delete_cluster(self, args):
        results = self.client.delete_cluster(
            ClusterIdentifier=args['CLUSTER_ID'],
            SkipFinalClusterSnapshot=False,
            FinalClusterSnapshotIdentifier=args['CLUSTER_ID'] + str(
                uuid.uuid1()),
            FinalClusterSnapshotRetentionPeriod=2
        )
        return self.update_status(results=results,
                                  name=args['CLUSTER_ID'],
                                  status="Deleting")

    @DatabaseUpdate()
    def resize_cluster_node_count(self, args):
        results = self.client.modify_cluster(
            ClusterIdentifier=args['CLUSTER_ID'],
            ClusterType=args['type'],
            NumberOfNodes=int(args['nodes']),
        )

        return self.update_status(results=results,
                                  name=args['CLUSTER_ID'],
                                  status="resizing")

    @DatabaseUpdate()
    def resize_cluster_to_multi_node(self, args):
        results = self.client.modify_cluster(
            ClusterIdentifier=args['CLUSTER_ID'],
            ClusterType=args['type'],
            NumberOfNodes=int(args['nodes']),
            NodeType=args['nodetype']
        )

        return self.update_status(results=results,
                                  name=args['CLUSTER_ID'],
                                  status="Changing node count")

    @DatabaseUpdate()
    def resize_cluster_node_types(self, args):
        results = self.client.modify_cluster(
            ClusterIdentifier=args['CLUSTER_ID'],
            NodeType=args['nodetype'],
            NumberOfNodes=int(args['nodes'])
        )
        return self.update_status(results=results,
                                  name=args['CLUSTER_ID'],
                                  status="Changing node types")

    @DatabaseUpdate()
    def modify_cluster(self, args):
        VERBOSE("in modify")
        results = self.client.modify_cluster(
            ClusterIdentifier=args['CLUSTER_ID'],
            MasterUserPassword=args['newpass']
        )
        return self.update_status(results=results,
                                  name=args['CLUSTER_ID'],
                                  status="Modifying password")

    @DatabaseUpdate()
    def rename_cluster(self, args):
        VERBOSE("in rename")
        results = self.client.modify_cluster(
            ClusterIdentifier=args['CLUSTER_ID'],
            NewClusterIdentifier=args['newid'],
        )
        return self.update_status(results=results,
                                  name=args['CLUSTER_ID'],
                                  status="Renaming")

        # {'describe': False, 'CLUSTER_ID': 'cl13',
        #  'create': False, 'DB_NAME': None, 'USER_NAME': None, 'PASSWD': None, '--nodetype': 'dc1.large',
        #  '--type': 'single-node', '--nodes': '1',
        #  'resize': False, 'modify': True, '--newid': 'cl14', '--newpass': None,
        #  'delete': False,
        #  'type': 'single-node', 'nodetype': 'dc1.large', 'nodes': '1', 'newid': 'cl14', 'newpass': None}
        #

    #
    # BUG functiosnto create the db and to interact with it through a query are missing
    #
