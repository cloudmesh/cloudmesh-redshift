from cloudmesh.management.configuration.config import Config
import uuid
import boto3
from botocore.exceptions import ClientError, ParamValidationError

from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate


class Manager(object):

    def __init__(self):
        # self.opt_states = {'start': 'STARTING', 'boot': 'BOOTSTRAPPING', 'run': 'RUNNING', 'wait': 'WAITING',
        #               'terminating': 'TERMINATING', 'shutdown': 'TERMINATED', 'error': 'TERMINATED_WITH_ERRORS'}

        return

    def get_client(self, service='redshift'):
        configs = Config()

        key_id = configs['cloudmesh.cloud.aws.credentials.EC2_ACCESS_ID']
        access_key = configs['cloudmesh.cloud.aws.credentials.EC2_SECRET_KEY']
        region = configs['cloudmesh.cloud.aws.credentials.region']

        client = boto3.client(service, region_name=region,
                              aws_access_key_id=key_id,
                              aws_secret_access_key=access_key)
        return client

    # def parse_options(self, options, states):
    #     result = []
    #
    #     if 'all' not in options:
    #         for option in options:
    #             if option in states:
    #                 result += [states[option]]
    #     return result

    # @DatabaseUpdate()
    def describe_clusters(self, args):
        client = self.get_client()
        # results = client.describe_clusters()
        #
        # return results['Clusters']

        try:
            results = client.describe_clusters()
            return results['Clusters']
        except ClientError as e:
            if e.response['Error']['Code'] == 'ClusterNotFound':
                return "Cluster not found"
            else:
                return "Unexpected error: %s" % e

    # @DatabaseUpdate()
    def describe_cluster(self, args):
        client = self.get_client()

        try:
            results = client.describe_clusters(ClusterIdentifier=args['CLUSTER_ID'])
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

    # @DatabaseUpdate()
    def create_single_node_cluster(self, args):
        client = self.get_client()

        results = client.create_cluster(
            DBName=args['DB_NAME'],
            ClusterIdentifier=args['CLUSTER_ID'],
            ClusterType='single-node',
            NodeType=args['NODE_TYPE'],
            MasterUsername=args['USERNAME'],
            MasterUserPassword=args['PASSWD'],
            Port=5439,
            AllowVersionUpgrade=True,
            # NumberOfNodes=1, # needs to be supplied if ClusterType is multi-node
            PubliclyAccessible=True,
            Encrypted=False
        )

        return {"cloud": "aws", "kind": "redshift", "cluster": results, "name": args['CLUSTER_ID'],
                "status": "Creating"}

    # @DatabaseUpdate()
    def create_multi_node_cluster(self, args):
        client = self.get_client()

        # database
        # create[—-dbname = NAME]
        # [—-dbtype = DBS]
        # [--username = USERNAME]
        # [—-passwd = PASSWD]
        # [—-nodes = NUM]
        # [--secgroup = SECGROUPs]
        # [—-tags = TAGS]

        results = client.create_cluster(
            DBName=args['DB_NAME'],
            ClusterIdentifier=args['CLUSTER_ID'],
            ClusterType='multi-node',
            NodeType=args['NODE_TYPE'],
            MasterUsername=args['USERNAME'],
            MasterUserPassword=args['PASSWD'],
            Port=5439,
            AllowVersionUpgrade=True,
            NumberOfNodes=args['NODE_NUM'],
            PubliclyAccessible=True,
            Encrypted=False
        )

        return {"cloud": "aws", "kind": "redshift", "cluster": results, "name": args['CLUSTER_ID'],
                "status": "Creating"}

    # @DatabaseUpdate()
    def delete_cluster(self, args):
        client = self.get_client()

        results = client.delete_cluster(
            ClusterIdentifier=args['CLUSTER_ID'],
            SkipFinalClusterSnapshot=False,
            FinalClusterSnapshotIdentifier=args['CLUSTER_ID'] + str(uuid.uuid1()),
            FinalClusterSnapshotRetentionPeriod=2
        )

        return {"cloud": "aws", "kind": "redshift", "cluster": results, "name": args['CLUSTER_ID'],
                "status": "Deleting"}

    # @DatabaseUpdate()
    def resize_cluster_nodes(self, args):
        client = self.get_client()

        results = client.modify_cluster(
            ClusterIdentifier=args['CLUSTER_ID'],
            ClusterType=args['CLUSTER_TYPE'],
            NumberOfNodes=args['NODE_NUM'],
        )

        return {"cloud": "aws", "kind": "redshift", "cluster": results, "name": args['CLUSTER_ID'],
                "status": "Resizing"}

    # @DatabaseUpdate()
    # def resize_cluster_to_multi_node(self, args):
    #     client = self.get_client()
    #
    #     results = client.modify_cluster(
    #         ClusterIdentifier=args['CLUSTER_ID'],
    #         ClusterType=args['CLUSTER_TYPE'],
    #         NumberOfNodes=args['NODE_NUM']
    #     )
    #
    #     return {"cloud": "aws", "kind": "redshift", "cluster": results, "name": args['CLUSTER_ID'],
    #             "status": "Resizing"}

    # @DatabaseUpdate()
    def resize_cluster_node_types(self, args):
        client = self.get_client()

        results = client.modify_cluster(
            ClusterIdentifier=args['CLUSTER_ID'],
            NodeType=args['NODE_TYPE'],
            NumberOfNodes=args['NODE_NUM']
        )

        return {"cloud": "aws", "kind": "redshift", "cluster": results, "name": args['CLUSTER_ID'],
                "status": "Resizing"}

    # @DatabaseUpdate()
    def modify_cluster(self, args):
        client = self.get_client()

        results = client.modify_cluster(
            ClusterIdentifier=args['CLUSTER_ID'],
            MasterUserPassword=args['PASSWD'],
        )

        return {"cloud": "aws", "kind": "redshift", "cluster": results, "name": args['CLUSTER_ID'],
                "status": "Modifying"}

    # @DatabaseUpdate()
    def rename_cluster(self, args):
        client = self.get_client()

        results = client.modify_cluster(
            ClusterIdentifier=args['CLUSTER_ID'],
            NewClusterIdentifier=args['NEW_CLUSTER_ID'],
        )

        return {"cloud": "aws", "kind": "redshift", "cluster": results, "name": args['CLUSTER_ID'],
                "status": "Renaming"}
