from cloudmesh.management.configuration.config import Config
import uuid
import boto3
from botocore.exceptions import ClientError
from cloudmesh.DEBUG import VERBOSE
from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate
import psycopg2
import re
import base64

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
    def describe_clusters(self):
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
    def describe_cluster(self, cluster_id):
        try:
            results = self.client.describe_clusters(
                ClusterIdentifier=cluster_id)
            print(results['Clusters'])
            return [{"cm": {"cloud": "aws", "kind": "redshift", "name": cluster_id},
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
    def create_single_node_cluster(self, db_name, cluster_id, cluster_type, node_type, user_name, passwd):
        print("In single node")
        if cluster_type is None:
            cluster_type = 'single-node'

        # print(args)
        results = self.client.create_cluster(
            DBName=db_name,
            ClusterIdentifier=cluster_id,
            ClusterType=cluster_type,
            NodeType=node_type,
            MasterUsername=user_name,
            MasterUserPassword=passwd,
            Port=5439,
            AllowVersionUpgrade=True,
            # NumberOfNodes=1, # needs to be supplied if ClusterType is multi-node
            PubliclyAccessible=True,
            Encrypted=False
        )
        print(results)
        return self.update_status(results=results,
                                  name=cluster_id,
                                  status="Creating")


    @DatabaseUpdate()
    def create_multi_node_cluster(self, db_name, cluster_id, cluster_type, node_type, user_name, passwd, node_count):

        if cluster_type is None:
            cluster_type = 'multi-node'

        results = self.client.create_cluster(
            DBName=db_name,
            ClusterIdentifier=cluster_id,
            ClusterType=cluster_type,
            NodeType=node_type,
            MasterUsername=user_name,
            MasterUserPassword=passwd,
            Port=5439,
            AllowVersionUpgrade=True,
            NumberOfNodes=node_count,
            PubliclyAccessible=True,
            Encrypted=False
        )
        return self.update_status(results=results,
                                  name=cluster_id,
                                  status="Creating")

    @DatabaseUpdate()
    def delete_cluster(self, cluster_id):
        results = self.client.delete_cluster(
            ClusterIdentifier=cluster_id,
            SkipFinalClusterSnapshot=False,
            FinalClusterSnapshotIdentifier=cluster_id + str(uuid.uuid1()),
            FinalClusterSnapshotRetentionPeriod=2
        )
        return self.update_status(results=results,
                                  name=cluster_id,
                                  status="Deleting")

    @DatabaseUpdate()
    def resize_cluster_node_count(self, cluster_id, cluster_type, node_count):
        results = self.client.modify_cluster(
            ClusterIdentifier=cluster_id,
            ClusterType=cluster_type,
            NumberOfNodes=node_count,
        )

        return self.update_status(results=results,
                                  name=cluster_id,
                                  status="resizing")

    @DatabaseUpdate()
    def resize_cluster_to_multi_node(self, cluster_id, cluster_type, node_count, node_type):
        results = self.client.modify_cluster(
            ClusterIdentifier=cluster_id,
            ClusterType=cluster_type,
            NumberOfNodes=node_count,
            NodeType=node_type
        )

        return self.update_status(results=results,
                                  name=cluster_id,
                                  status="Changing node count")

    @DatabaseUpdate()
    def resize_cluster_node_types(self, cluster_id, node_type, node_count):
        results = self.client.modify_cluster(
            ClusterIdentifier=cluster_id,
            NodeType=node_type,
            NumberOfNodes=node_count
        )
        return self.update_status(results=results,
                                  name=cluster_id,
                                  status="Changing node types")

    @DatabaseUpdate()
    def modify_cluster(self, cluster_id, new_pass):
        VERBOSE("in modify")
        results = self.client.modify_cluster(
            ClusterIdentifier=cluster_id,
            MasterUserPassword=new_pass
        )
        return self.update_status(results=results,
                                  name=cluster_id,
                                  status="Modifying password")

    @DatabaseUpdate()
    def rename_cluster(self, cluster_id, new_id):
        VERBOSE("in rename")
        results = self.client.modify_cluster(
            ClusterIdentifier=cluster_id,
            NewClusterIdentifier=new_id,
        )
        return self.update_status(results=results,
                                  name=cluster_id,
                                  status="Renaming")

    @DatabaseUpdate()
    def allow_access(self, cluster_id):
        VERBOSE("in allow access")
        desc_response = self.client.describe_clusters(
            ClusterIdentifier=cluster_id
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
                                  name=cluster_id,
                                  status="Allowing access")

    @DatabaseUpdate()
    def create_demo_schema(self, cluster_id, db_name, host, port, user_name, passwd):
        VERBOSE("in create schema demo")
        print("in create demo schema")
        results = "Error"
        try:
            conn = psycopg2.connect(dbname=db_name, host=host, port=port,
                                    user=user_name, password=passwd)

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
                print("Error executing sql", err)
                cur.close()
                conn.close()
                return self.update_status(results=results,
                                      name=cluster_id,
                                      status="Unable to execute query")

            return self.update_status(results=results,
                                      name=cluster_id,
                                      status="Query results")

        except Exception as err:
            print("unable to connect")
            print("Unable to connect", err)
            return self.update_status(results=results,
                                      name=cluster_id,
                                      status="Unable to connect")
    @DatabaseUpdate()
    def delete_demo_schema(self,  cluster_id, db_name, host, port, user_name, passwd):
        VERBOSE("in delete demo")
        print("in delete demo schema")
        results = "Error"
        try:
            conn = psycopg2.connect(dbname=db_name, host=host, port=port,
                                    user=user_name, password=passwd)

            cur = conn.cursor()
            sql = "DROP TABLE emp;"
            try:
                cur.execute(sql)
                results = "Successfully deleted demo schema"
                cur.close()
                conn.commit()
                conn.close()
            except Exception as err:
                print("Unable to execute", err)
                cur.close()
                conn.close()
                return self.update_status(results=results,
                                      name=cluster_id,
                                      status="Unable to execute query")

            return self.update_status(results=results,
                                      name=cluster_id,
                                      status="Query results")

        except Exception as err:
            print("Unable to connect", err)
            return self.update_status(results=results,
                                      name=cluster_id,
                                      status="Unable to connect")


    @DatabaseUpdate()
    def runselectquery_text(self, cluster_id, db_name, host, port, user_name, passwd, query_text):
        VERBOSE("in runselectquery")
        print("In runselectquerytext")
        # print(args)
        results = "Error"
        try:
            conn = psycopg2.connect(dbname=db_name, host=host, port=port,
                                    user=user_name, password=passwd)

            cur = conn.cursor()

            print(query_text)
            sql = query_text

            try:
                cur.execute(sql)
                results = cur.fetchall()
                print(results)
                cur.close()
                conn.close()
            except Exception as err:
                print("unable to execute query")
                print("Unable to execute", err)
                cur.close()
                conn.close()
                return self.update_status(results=results,
                                      name=cluster_id,
                                      status="Unable to execute query")

            return self.update_status(results=results,
                                      name=cluster_id,
                                      status="Query results")

        except Exception as err:
            print("unable to connect")
            print("Unable to connect", err)
            return self.update_status(results=results,
                                      name=cluster_id,
                                      status="Unable to connect")
    @DatabaseUpdate()
    def runddl(self, cluster_id, db_name, host, port, user_name, passwd, b64_sql_file_contents):
        VERBOSE("in runsql - DDL")
        print("In runsql - DDL")
        # print(args)
        results = "Error"
        try:
            conn = psycopg2.connect(dbname=db_name, host=host, port=port,
                                    user=user_name, password=passwd)

            cur = conn.cursor()

            sql_file_contents = base64.b64decode(b64_sql_file_contents).decode('ascii')
            # in the future for DML, we may need to base64.b64decode(b64_sql_file_contents).decode("utf-8", "ignore")
            # all SQL statements (split on ';')
            sql_stmts = sql_file_contents.split(';')

            for stmt in sql_stmts:
                # This will skip and report errors
                # For example, if the tables do not yet exist, this will skip over
                # the DROP TABLE commands
                if stmt is None or len(stmt.strip()) == 0:
                    continue
                try:
                    cur.execute(stmt)
                except psycopg2.InterfaceError as err:
                    print("error in interface:", err)
                    conn.rollback()
                    continue
                except psycopg2.DatabaseError as err:
                    print("error related to DB:", err)
                    conn.rollback()
                    continue
                except psycopg2.DataError as err:
                    print("error in data:", err)
                    conn.rollback()
                    continue
                except psycopg2.OperationalError as err:
                    print("error related to db operation:", err)
                    conn.rollback()
                    continue
                except psycopg2.IntegrityError as err:
                    print("error in data integrity:", err)
                    conn.rollback()
                    continue
                except psycopg2.InternalError as err:
                    print("error: internal, usually type of DB Error:", err)
                    conn.rollback()
                    continue
                except psycopg2.ProgrammingError as err:
                    print("error in Programming:", err)
                    conn.rollback()
                    continue
                except psycopg2.NotSupportedError as err:
                    print("error - not supported feature/operation: ", err)
                    conn.rollback()
                    continue

            cur.close()
            conn.close()
            return self.update_status(results=results,
                                  name=cluster_id,
                                  status="SQL Execution")


        except Exception as err:
            print("unable to connect")
            print("Unable to connect", err)
            return self.update_status(results=results,
                                      name=cluster_id,
                                      status="Unable to connect")

    @DatabaseUpdate()
    def rundml(self, cluster_id, db_name, host, port, user_name, passwd, b64_sql_file_contents):
        VERBOSE("in runsql - DML")
        print("In runsql - DML")
        # print(args)
        results = "Error"
        try:
            conn = psycopg2.connect(dbname=db_name, host=host, port=port,
                                    user=user_name, password=passwd)

            cur = conn.cursor()

            sql_file_contents = base64.b64decode(b64_sql_file_contents).decode('utf-8')
            # in the future for DML, we may need to base64.b64decode(b64_sql_file_contents).decode("utf-8", "ignore")
            # all SQL statements (split on ';')
            sql_stmts = sql_file_contents.split(';')

            for stmt in sql_stmts:
                # This will skip and report errors
                # For example, if the tables do not yet exist, this will skip over
                # the DROP TABLE commands
                if stmt is None or len(stmt.strip()) == 0:
                    continue
                try:
                    cur.execute(stmt)
                except psycopg2.InterfaceError as err:
                    print("error in interface:", err)
                except psycopg2.DatabaseError as err:
                    print("error related to DB:", err)
                except psycopg2.DataError as err:
                    print("error in data:", err)
                except psycopg2.OperationalError as err:
                    print("error related to db operation:", err)
                except psycopg2.IntegrityError as err:
                    print("error in data integrity:", err)
                except psycopg2.InternalError as err:
                    print("error: internal, usually type of DB Error:", err)
                except psycopg2.ProgrammingError as err:
                    print("error in Programming:", err)
                except psycopg2.NotSupportedError as err:
                    print("error - not supported feature/operation: ", err)

            cur.close()
            conn.close()
            return self.update_status(results=results,
                                  name=cluster_id,
                                  status="SQL Execution")


        except Exception as err:
            print("unable to connect")
            print("Unable to connect", err)
            return self.update_status(results=results,
                                      name=cluster_id,
                                      status="Unable to connect")


if __name__ == "__main__":
    print("In Provider")
