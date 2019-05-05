# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.red_shift_cluster import RedShiftCluster  # noqa: E501
from swagger_server.test import BaseTestCase


class TestClusterController(BaseTestCase):
    """ClusterController integration test stubs"""

    def test_cloudmesh_redshift_provider_allow_access(self):
        """Test case for cloudmesh_redshift_provider_allow_access

        Allow external access to cluster
        """
        response = self.client.open(
            '/cloudmesh/redshift/v1/cluster/{clusterId}/allowaccess'.format(clusterId='clusterId_example'),
            method='PATCH',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cloudmesh_redshift_provider_change_node_type(self):
        """Test case for cloudmesh_redshift_provider_change_node_type

        Change  node type
        """
        query_string = [('clusterType', 'clusterType_example'),
                        ('nodeType', 'dc2.large')]
        response = self.client.open(
            '/cloudmesh/redshift/v1/cluster/{clusterId}/changenodetype'.format(clusterId='clusterId_example'),
            method='PATCH',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cloudmesh_redshift_provider_chg_password(self):
        """Test case for cloudmesh_redshift_provider_chg_password

        Change master password
        """
        query_string = [('newPass', 'newPass_example')]
        response = self.client.open(
            '/cloudmesh/redshift/v1/cluster/{clusterId}/changepassword'.format(clusterId='clusterId_example'),
            method='PATCH',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cloudmesh_redshift_provider_create_multi_node_cluster(self):
        """Test case for cloudmesh_redshift_provider_create_multi_node_cluster

        Creates a cluster
        """
        query_string = [('dbName', 'dbName_example'),
                        ('masterUserName', 'masterUserName_example'),
                        ('passWord', 'passWord_example'),
                        ('nodeType', 'dc2.large'),
                        ('clusterType', 'multi-node'),
                        ('nodeCount', 2)]
        response = self.client.open(
            '/cloudmesh/redshift/v1/cluster/{clusterId}'.format(clusterId='clusterId_example'),
            method='POST',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cloudmesh_redshift_provider_delete_cluster(self):
        """Test case for cloudmesh_redshift_provider_delete_cluster

        Deletes a cluster
        """
        response = self.client.open(
            '/cloudmesh/redshift/v1/cluster/{clusterId}'.format(clusterId='clusterId_example'),
            method='DELETE',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cloudmesh_redshift_provider_describe_cluster(self):
        """Test case for cloudmesh_redshift_provider_describe_cluster

        Describe cluster by ID
        """
        response = self.client.open(
            '/cloudmesh/redshift/v1/cluster/{clusterId}'.format(clusterId='clusterId_example'),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cloudmesh_redshift_provider_describe_clusters(self):
        """Test case for cloudmesh_redshift_provider_describe_clusters

        Describe all clusters
        """
        response = self.client.open(
            '/cloudmesh/redshift/v1/clusters',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cloudmesh_redshift_provider_rename_cluster(self):
        """Test case for cloudmesh_redshift_provider_rename_cluster

        Rename cluster
        """
        query_string = [('newId', 'newId_example')]
        response = self.client.open(
            '/cloudmesh/redshift/v1/cluster/{clusterId}/rename'.format(clusterId='clusterId_example'),
            method='PATCH',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cloudmesh_redshift_provider_resize_cluster(self):
        """Test case for cloudmesh_redshift_provider_resize_cluster

        Increases cluster nodes
        """
        query_string = [('clusterType', 'multi-node'),
                        ('nodeCount', 2),
                        ('nodeType', 'dc2.large')]
        response = self.client.open(
            '/cloudmesh/redshift/v1/cluster/{clusterId}/resize'.format(clusterId='clusterId_example'),
            method='PATCH',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cloudmesh_redshift_provider_runddl(self):
        """Test case for cloudmesh_redshift_provider_runddl

        Runs DDL on cluster
        """
        query_string = [('dbName', 'dbName_example'),
                        ('host', 'host_example'),
                        ('port', 5439),
                        ('userName', 'userName_example'),
                        ('passWord', 'passWord_example'),
                        ('sql_file_contents', 'sql_file_contents_example')]
        response = self.client.open(
            '/cloudmesh/redshift/v1/cluster/{clusterId}/runDDL'.format(clusterId='clusterId_example'),
            method='PATCH',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cloudmesh_redshift_provider_rundml(self):
        """Test case for cloudmesh_redshift_provider_rundml

        Runs DML on cluster
        """
        query_string = [('dbName', 'dbName_example'),
                        ('host', 'host_example'),
                        ('port', 5439),
                        ('userName', 'userName_example'),
                        ('passWord', 'passWord_example'),
                        ('sql_file_contents', 'sql_file_contents_example')]
        response = self.client.open(
            '/cloudmesh/redshift/v1/cluster/{clusterId}/runDML'.format(clusterId='clusterId_example'),
            method='PATCH',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cloudmesh_redshift_provider_runquery(self):
        """Test case for cloudmesh_redshift_provider_runquery

        Runs a query on the cluster
        """
        query_string = [('dbName', 'dbName_example'),
                        ('host', 'host_example'),
                        ('port', 5439),
                        ('userName', 'userName_example'),
                        ('passWord', 'passWord_example'),
                        ('queryText', 'queryText_example')]
        response = self.client.open(
            '/cloudmesh/redshift/v1/cluster/{clusterId}/runQuery'.format(clusterId='clusterId_example'),
            method='PATCH',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
