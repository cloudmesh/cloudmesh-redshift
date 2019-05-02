from cloudmesh.management.configuration.config import Config
import uuid
import boto3
from botocore.exceptions import ClientError
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate
import psycopg2
import re

class Provider(object):

    def __init__(self, service='redshift', config="~/.cloudmesh/cloudmesh4.yaml"):
        VERBOSE("initialize redshift manager")
        self.key_id = None
        self.access_key = None
        self.region = None
        self.config = Config(config_path=config)

        print(self.key_id)
        self.key_id = self.config[
            'cloudmesh.cloud.aws.credentials.EC2_ACCESS_ID']
        self.access_key = self.config[
            'cloudmesh.cloud.aws.credentials.EC2_SECRET_KEY']
        self.region = self.config['cloudmesh.cloud.aws.credentials.region']

        self.client = boto3.client(
            service,
            region_name=self.region,
            aws_access_key_id=self.key_id,
            aws_secret_access_key=self.access_key
        )
        # print(self.key_id)

        self.ec2_client = boto3.client(
            'ec2',
            region_name=self.region,
            aws_access_key_id=self.key_id,
            aws_secret_access_key=self.access_key
        )

        self.ec2_resource = boto3.resource(
            'ec2',
            region_name=self.region,
            aws_access_key_id=self.key_id,
            aws_secret_access_key=self.access_key
        )


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

    # def update_dict(self, elements, kind=None):
    #     # this is an internal function for building dict object
    #     d = []
    #     for element in elements:
    #         #entry = element.__dict__
    #         #entry = element['objlist']
    #         entry = element
    #         entry["cm"] = {
    #             "kind": "storage",
    #             "cloud": self.cloud,
    #             "name": entry['fileName']
    #         }
    #
    #         # element.properties = element.properties.__dict__
    #         d.append(entry)
    #     return d

    def update_status(self, results=None, name=None, status=None):
        return self.update_dict(
            {"cloud": "aws",
             "kind": "redshift",
             "name": name,
             "status": status,
             "results":results,
             })

    #
    # BUG: all dicts that go in teh db must be updated woth update_dict
    #      afterthat the @DatabaseUpdate will work

    @DatabaseUpdate()
    def describe_clusters(self, args):
        try:
            results = self.client.describe_clusters()
            print(results['Clusters'])
            return [{"cm": {"cloud": "aws", "kind": "redshift", "name": "all"}, 'results': results['Clusters']}]

        except ClientError as e:
            if e.response['Error']['Code'] == 'ClusterNotFound':
                return "Cluster not found"
            else:
                return "Unexpected error: %s" % e

    #
    # BUG: all dicts that go in teh db must be updated woth update_dict
    #      afterthat the @DatabaseUpdate will work

    @DatabaseUpdate()
    def describe_cluster(self, args):
        try:
            results = self.client.describe_clusters(
                ClusterIdentifier=args['CLUSTER_ID'])
            print(results['Clusters'])
            return [{"cm": {"cloud": "aws", "kind": "redshift", "name": args['CLUSTERID']},
                    'results': results['Clusters']}]
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
        print("In single node")
        if args.get('CLUSTER_TYPE') is not None:
            cluster_type = args['CLUSTER_TYPE']
        else:
            cluster_type = 'single-node'

        print(args)
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
        print(results)
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

    @DatabaseUpdate()
    def allow_access(self, args):
        VERBOSE("in allow access")
        desc_response = self.client.describe_clusters(
            ClusterIdentifier=args['CLUSTER_ID']
        )

        # print(desc_response['Clusters'][0]['VpcId'])
        vpc_id = desc_response['Clusters'][0]['VpcId']

        vpc = self.ec2_resource.Vpc(vpc_id)

        security_group_iterator = vpc.security_groups.all()
        # print(security_group_iterator)
        for s in security_group_iterator:
            print(s)

        security_group_iterator2 = vpc.security_groups.filter(
            GroupNames=[
                'default',
            ]
        )
        print(security_group_iterator2)
        for s2 in security_group_iterator2:
            print(s2)

        grp_id_list = re.findall(r"'(.*?)'", str(s2), re.DOTALL)
        grp_id = grp_id_list[0]
        # print(grp_id)

        security_group = self.ec2_resource.SecurityGroup(grp_id)

        sec_grp_ingress_response = security_group.authorize_ingress(
            GroupId=grp_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 5439,
                    'ToPort': 5439,
                    'IpRanges': [
                        {
                            'CidrIp': '0.0.0.0/0',
                            'Description': 'all ext'
                        },
                    ],
                    'UserIdGroupPairs': [{'GroupId': grp_id, 'VpcId': vpc_id}]
                }
            ],
        )
        results = sec_grp_ingress_response
        # print(sec_grp_ingress_response)

        return self.update_status(results=results,
                                  name=args['CLUSTER_ID'],
                                  status="Allowing access")

    @DatabaseUpdate()
    def create_demo_schema(self, args):
        VERBOSE("in create schema demo")
        print("in create demo schema")
        results = "Error"
        try:
            conn = psycopg2.connect(dbname=args['DB_NAME'], host=args['HOST'], port=args['PORT'],
                                    user=args['USER_NAME'], password=args['PASSWD'])

            print("connected")
            cur = conn.cursor()
            sql_cr = "CREATE TABLE emp (empid INT, empname VARCHAR(80));"
            sql_ins1 = "INSERT INTO emp values (10, 'smith');"
            sql_ins2 = "INSERT INTO emp values (20, 'jones');"
            sql_ins3 = "INSERT INTO emp values (30, 'scott');"
            sql_ins4 = "INSERT INTO emp values (40, 'adams');"

            try:
                print("exec sql")
                cur.execute(sql_cr)
                cur.execute(sql_ins1)
                cur.execute(sql_ins2)
                cur.execute(sql_ins3)
                cur.execute(sql_ins4)
                results = "Successfully created demo schema"
                cur.close()
                conn.commit()
                conn.close()
            except Exception as err:
                print("err executing sql")
                print(err.code, err)
                cur.close()
                conn.close()
                return self.update_status(results=results,
                                      name=args['CLUSTER_ID'],
                                      status="Unable to execute query")

            return self.update_status(results=results,
                                      name=args['CLUSTER_ID'],
                                      status="Query results")

        except Exception as err:
            print("unable to connect")
            print(err.code, err)
            return self.update_status(results=results,
                                      name=args['CLUSTER_ID'],
                                      status="Unable to connect")
    @DatabaseUpdate()
    def delete_demo_schema(self, args):
        VERBOSE("in delete demo")
        print("in delete demo schema")
        results = "Error"
        try:
            conn = psycopg2.connect(dbname=args['DB_NAME'], host=args['HOST'], port=args['PORT'],
                                    user=args['USER_NAME'], password=args['PASSWD'])

            cur = conn.cursor()
            sql = "DROP TABLE emp;"
            try:
                cur.execute(sql)
                results = "Successfully deleted demo schema"
                cur.close()
                conn.commit()
                conn.close()
            except Exception as err:
                print(err.code, err)
                cur.close()
                conn.close()
                return self.update_status(results=results,
                                      name=args['CLUSTER_ID'],
                                      status="Unable to execute query")

            return self.update_status(results=results,
                                      name=args['CLUSTER_ID'],
                                      status="Query results")

        except Exception as err:
            print(err.code, err)
            return self.update_status(results=results,
                                      name=args['CLUSTER_ID'],
                                      status="Unable to connect")


    @DatabaseUpdate()
    def runselectquery_text(self, args):
        VERBOSE("in runselectquery")
        print("In runselectquerytext")
        print(args)
        results = "Error"
        try:
            conn = psycopg2.connect(dbname=args['DB_NAME'], host=args['HOST'], port=args['PORT'],
                                    user=args['USER_NAME'], password=args['PASSWD'])

            cur = conn.cursor()

            print(args['querytext'])
            sql = args['querytext']

            try:
                cur.execute(sql)
                results = cur.fetchall()
                print(results)
                cur.close()
                conn.close()
            except Exception as err:
                print("unable to execute query")
                print(err.code, err)
                cur.close()
                conn.close()
                return self.update_status(results=results,
                                      name=args['CLUSTER_ID'],
                                      status="Unable to execute query")

            return self.update_status(results=results,
                                      name=args['CLUSTER_ID'],
                                      status="Query results")

        except Exception as err:
            print("unable to connect")
            print(err.code, err)
            return self.update_status(results=results,
                                      name=args['CLUSTER_ID'],
                                      status="Unable to connect")



if __name__ == "__main__":
    print("In Provider")
