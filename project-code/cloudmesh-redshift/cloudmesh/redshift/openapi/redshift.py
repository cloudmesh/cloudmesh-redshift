from __future__ import print_function
from cloudmesh.redshift.api.manager import Manager


def describe_clusters():
    redshift = Manager()

    result = redshift.describe_clusters()
    print(result)

    return result


def describe_cluster(clusterId):
    redshift = Manager()

    result = redshift.describe_cluster({'CLUSTER_ID': clusterId})
    print(result)

    return result

def create_multi_node_cluster(clusterId, dbName, masterUserName, passWord, nodeType, clusterType, nodeCount):
    redshift = Manager()

    result = redshift.create_multi_node_cluster({'CLUSTER_ID': clusterId,
                                                 'DB_NAME': dbName,
                                                 'USER_NAME': masterUserName,
                                                 'PASSWD': passWord,
                                                 'nodetype': nodeType,
                                                 'CLUSTER_TYPE': clusterType,
                                                 'nodes': int(nodeCount)})

    print(result)
    return result


def delete_cluster(clusterId):
    redshift = Manager()
    result = redshift.delete_cluster({'CLUSTER_ID':clusterId})
    print(result)
    return result

def resize_cluster(clusterId, clusterType, nodeCount, nodeType):
    redshift = Manager()
    result = redshift.resize_cluster_node_count({'CLUSTER_ID': clusterId, 'nodetype': nodeType, 'CLUSTER_TYPE': clusterType,
                                                 'nodes': int(nodeCount)})
    print(result)
    return result

def change_node_type(clusterId, clusterType, nodeType):
    redshift = Manager()
    result = redshift.resize_cluster_node_types({'CLUSTER_ID': clusterId, 'nodetype': nodeType, 'CLUSTER_TYPE': clusterType})
    print(result)
    return result

def rename_cluster(clusterId, newId):
    redshift = Manager()
    result = redshift.rename_cluster({'CLUSTER_ID':clusterId, 'newid': newId})
    print(result)
    return result

def chg_password(clusterId, newPass):
    redshift = Manager()
    result = redshift.modify_cluster({'CLUSTER_ID':clusterId, 'newpass': newPass})
    print(result)
    return result

