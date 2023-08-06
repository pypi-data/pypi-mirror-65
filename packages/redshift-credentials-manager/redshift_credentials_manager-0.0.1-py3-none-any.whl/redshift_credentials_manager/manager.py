from datetime import datetime, timedelta
from typing import List

import boto3


class RedshiftCredentialsManager(object):
    def __init__(self, cluster_id: str, user: str, database_name: str, groups:
                 List[str] =None,
                 auto_create=True, grace_period=None, boto_session=None):
        self.cluster_id = cluster_id
        self.user = user
        self.database_name = database_name
        self.groups = groups or []
        self.auto_create = True
        self._credential_expiration = datetime.max
        self._grace_period = grace_period or timedelta(seconds=1)
        self._connection_info = None
        self._credentials = None
        self._redshift_client = (boto_session or boto3).client("redshift")

    def connect_with(self, connect):
        def _connect():
            options = self._build_connection_options()
            return connect(**options)
        return _connect

    def _build_connection_options(self):
        host, port = self._get_connection_info()
        user, password = self._get_credentials()
        return dict(host=host, port=port, user=user, password=password,
                    dbname=self.database_name, sslmode="require")

    def _get_connection_info(self):
        if self._connection_info:
            return self._connection_info
        response = self._redshift_client.describe_clusters(ClusterIdentifier=self.cluster_id)
        try:
            clusters = response['Clusters']
            cluster = clusters[0]
            endpoint = cluster['Endpoint']
            self._connection_info = (endpoint['Address'], endpoint['Port'])
            return self._connection_info
        except IndexError:
            raise Exception(f"Cluster {self.cluster_id} not found")

    def _get_credentials(self):
        if self._credentials and self._credentials_are_valid():
            return self._credentials
        response = self._redshift_client.get_cluster_credentials(ClusterIdentifier=self.cluster_id,
                                         DbUser=self.user,
                                         DbName=self.database_name,
                                         DbGroups=self.groups,
                                         AutoCreate=self.auto_create)
        self._credentials = (response['DbUser'], response['DbPassword'])
        self._credential_expiration = response['Expiration']
        return self._credentials

    def _credentials_are_valid(self):
        return datetime.now() + self._grace_period < self._credential_expiration

    def connect(connect):
        return connect(**self._build_connection_options())

