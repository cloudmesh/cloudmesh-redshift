import connexion
import six

from swagger_server.models.red_shift_cluster import RedShiftCluster  # noqa: E501
from swagger_server import util


def cloudmesh_redshift_provider_allow_access(clusterId):  # noqa: E501
    """Allow external access to cluster

    Allow external programs (eg Python) access to the Redshift cluster for queries # noqa: E501

    :param clusterId: ID of cluster to allow access to
    :type clusterId: str

    :rtype: RedShiftCluster
    """
    return 'do some magic!'


def cloudmesh_redshift_provider_change_node_type(clusterId, clusterType, nodeType=None):  # noqa: E501
    """Change  node type

     # noqa: E501

    :param clusterId: ID of cluster to update
    :type clusterId: str
    :param clusterType: Type of the cluster
    :type clusterType: str
    :param nodeType: Type of the node
    :type nodeType: str

    :rtype: RedShiftCluster
    """
    return 'do some magic!'


def cloudmesh_redshift_provider_chg_password(clusterId, newPass):  # noqa: E501
    """Change master password

    Change the password for the cluster # noqa: E501

    :param clusterId: ID of cluster to update
    :type clusterId: str
    :param newPass: New Password
    :type newPass: str

    :rtype: RedShiftCluster
    """
    return 'do some magic!'


def cloudmesh_redshift_provider_create_multi_node_cluster(clusterId, dbName, masterUserName, passWord, nodeType=None, clusterType=None, nodeCount=None):  # noqa: E501
    """Creates a cluster

     # noqa: E501

    :param clusterId: ID of cluster to be created
    :type clusterId: str
    :param dbName: Name of the DB
    :type dbName: str
    :param masterUserName: Master user name
    :type masterUserName: str
    :param passWord: Master user password
    :type passWord: str
    :param nodeType: Type of the node of the cluster
    :type nodeType: str
    :param clusterType: Type of the cluster
    :type clusterType: str
    :param nodeCount: Count of nodes in cluster
    :type nodeCount: 

    :rtype: None
    """
    return 'do some magic!'


def cloudmesh_redshift_provider_delete_cluster(clusterId):  # noqa: E501
    """Deletes a cluster

    Delete a cluster # noqa: E501

    :param clusterId: 
    :type clusterId: str

    :rtype: None
    """
    return 'do some magic!'


def cloudmesh_redshift_provider_describe_cluster(clusterId):  # noqa: E501
    """Describe cluster by ID

    Returns a single cluster description # noqa: E501

    :param clusterId: ID of cluster
    :type clusterId: str

    :rtype: RedShiftCluster
    """
    return 'do some magic!'


def cloudmesh_redshift_provider_describe_clusters():  # noqa: E501
    """Describe all clusters

    Detailed description of all cluster attributes # noqa: E501


    :rtype: RedShiftCluster
    """
    return 'do some magic!'


def cloudmesh_redshift_provider_rename_cluster(clusterId, newId):  # noqa: E501
    """Rename cluster

    Rename the cluster # noqa: E501

    :param clusterId: ID of cluster to rename
    :type clusterId: str
    :param newId: New ID for the cluster
    :type newId: str

    :rtype: RedShiftCluster
    """
    return 'do some magic!'


def cloudmesh_redshift_provider_resize_cluster(clusterId, clusterType=None, nodeCount=None, nodeType=None):  # noqa: E501
    """Increases cluster nodes

     # noqa: E501

    :param clusterId: ID of cluster to resize
    :type clusterId: str
    :param clusterType: Type of the cluster
    :type clusterType: str
    :param nodeCount: Count of nodes to resize cluster to
    :type nodeCount: 
    :param nodeType: Type of nodes 
    :type nodeType: str

    :rtype: RedShiftCluster
    """
    return 'do some magic!'


def cloudmesh_redshift_provider_runddl(clusterId, dbName, host, userName, passWord, sql_file_contents, port=None):  # noqa: E501
    """Runs DDL on cluster

    Run SQL Statements like CREATE TABLE, ALTER TABLE, DROP TABLE on the database # noqa: E501

    :param clusterId: ID of cluster 
    :type clusterId: str
    :param dbName: DB Name
    :type dbName: str
    :param host: Host name
    :type host: str
    :param userName: User name
    :type userName: str
    :param passWord: Password
    :type passWord: str
    :param sql_file_contents: Contents of an SQL file
    :type sql_file_contents: str
    :param port: Port number
    :type port: int

    :rtype: RedShiftCluster
    """
    return 'do some magic!'


def cloudmesh_redshift_provider_rundml(clusterId, dbName, host, userName, passWord, sql_file_contents, port=None):  # noqa: E501
    """Runs DML on cluster

    Run SQL Statements like INSERT, UPDATE, DELETE for data in the database # noqa: E501

    :param clusterId: ID of cluster 
    :type clusterId: str
    :param dbName: DB Name
    :type dbName: str
    :param host: Host name
    :type host: str
    :param userName: User name
    :type userName: str
    :param passWord: Password
    :type passWord: str
    :param sql_file_contents: Contents of an SQL file
    :type sql_file_contents: str
    :param port: Port number
    :type port: int

    :rtype: RedShiftCluster
    """
    return 'do some magic!'


def cloudmesh_redshift_provider_runquery(clusterId, dbName, host, userName, passWord, queryText, port=None):  # noqa: E501
    """Runs a query on the cluster

    Run SQL SELECT Statement # noqa: E501

    :param clusterId: ID of cluster 
    :type clusterId: str
    :param dbName: DB Name
    :type dbName: str
    :param host: Host name
    :type host: str
    :param userName: User name
    :type userName: str
    :param passWord: Password
    :type passWord: str
    :param queryText: SQL query
    :type queryText: str
    :param port: Port number
    :type port: int

    :rtype: RedShiftCluster
    """
    return 'do some magic!'
