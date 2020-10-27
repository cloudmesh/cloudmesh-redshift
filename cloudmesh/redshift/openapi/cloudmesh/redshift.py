from cloudmesh.redshift.Provider import Provider


def describe_clusters():
    redshift = Provider()

    result = redshift.describe_clusters({})
    print(result)

    return result


def describe_cluster(cluster_Id):
    redshift = Provider()

    result = redshift.describe_cluster({'CLUSTER_ID': cluster_Id})
    print(result)

    return result


def create_multi_node_cluster(cluster_id,
                              dbName,
                              masterUserName,
                              passWord,
                              nodeType,
                              clusterType,
                              nodeCount):
    redshift = Provider()

    result = redshift.create_multi_node_cluster({'CLUSTER_ID': cluster_id,
                                                 'DB_NAME': dbName,
                                                 'USER_NAME': masterUserName,
                                                 'PASSWD': passWord,
                                                 'nodetype': nodeType,
                                                 'CLUSTER_TYPE': clusterType,
                                                 'nodes': int(nodeCount)})

    print(result)
    return result


def delete_cluster(cluster_id):
    redshift = Provider()
    result = redshift.delete_cluster({'CLUSTER_ID': cluster_id})
    print(result)
    return result


def resize_cluster(cluster_id, clusterType, nodeCount, nodeType):
    redshift = Provider()
    result = redshift.resize_cluster_node_count({'CLUSTER_ID': cluster_id,
                                                 'nodetype': nodeType,
                                                 'CLUSTER_TYPE': clusterType,
                                                 'nodes': int(nodeCount)})
    print(result)
    return result


def change_node_type(cluster_id, clusterType, nodeType):
    redshift = Provider()
    result = redshift.resize_cluster_node_types({'CLUSTER_ID': cluster_id,
                                                 'nodetype': nodeType,
                                                 'CLUSTER_TYPE': clusterType})
    print(result)
    return result


def rename_cluster(cluster_id, newId):
    redshift = Provider()
    result = redshift.rename_cluster({'CLUSTER_ID': cluster_id,
                                      'newid': newId})
    print(result)
    return result


def chg_password(cluster_id, newPass):
    redshift = Provider()
    result = redshift.modify_cluster({'CLUSTER_ID': cluster_id,
                                      'newpass': newPass})
    print(result)
    return result
