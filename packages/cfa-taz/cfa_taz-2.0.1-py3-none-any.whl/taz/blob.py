#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Taz library: blobs operations

Examples:

get blob from sas key:

    blob = Blob(
        <container>, 
        <name>, 
        storage_account_name=<storage account_name
        sas_key=<sas key>)

get blob from sas url:

    blob = Blob(
        <container>, 
        <name>, 
        sas_url=<sas url>)

"""
import urllib
from azure.core.exceptions import ResourceExistsError

from azure.storage.blob import (
    BlobServiceClient,
    BlobClient,
    ContainerClient,
    BlobType,
    BlobSasPermissions,
    generate_blob_sas,
)
from datetime import datetime, timedelta
import pandas as pd
import gzip

from taz.exception import BlobAthenticationFailedException


class StorageAccount:
    def __init__(self, name, key=None, connection_string=None):
        """ Storage account object

        Args:
            name (TYPE): Description
            storage_key (None, optional): Description
        """

        self.name = name
        self.key = key
        self.connection_string = connection_string

        self.blob_service_client = BlobServiceClient.from_connection_string(
            self.connection_string
        )

    def list_containers(self, prefix=None):
        """ list storage account containers

        Returns:
            - azure.storage.blob.models.Container List: list of container, Container class attributes:
                - name
                - metadata
                - properties
        """
        return self.blob_service_client.list_containers(name_starts_with=prefix)


class Container:
    def __init__(self, storage_account, name):
        """ define Container object 

        Args:
            storage_account (TYPE): Description
            name (TYPE): Description
        """
        self.storage_account = storage_account
        self.name = name

        try:
            self.client = self.storage_account.blob_service_client.create_container(
                self.name
            )
        except ResourceExistsError:
            self.client = self.storage_account.blob_service_client.get_container_client(
                self.name
            )

    def get_properties(self):
        return self.client.get_container_properties()

    def delete(self):
        return self.storage_account.blob_service_client.delete_container(self.name)

    def list_blobs(self, prefix=None):
        return self.client.list_blobs(name_starts_with=prefix)


class Blob:
    def __init__(
        self,
        container,
        name,
        sas_url=None,
        sas_key=None,
        storage_account_name=None,
        storage_account=None,
    ):
        """define blob object
        
        :param container: container name
        :type container: str
        :param name: blob name
        :type name: str
        :param sas_url: sas url, defaults to None
        :type sas_url: str, optional
        :param sas_key: sas key (needs storage_account_name), defaults to None
        :type sas_key: str, optional
        :param storage_account_name: storage account name, defaults to None
        :type storage_account_name: str, optional
        :param storage_account: storage account object, defaults to None
        :type storage_account: taz.blob.StorageAccount, optional
        """
        self.storage_account = storage_account
        self.container = container
        self.name = name
        self.sas_url = sas_url
        self.storage_account = storage_account
        self.sas_key = sas_key
        self.storage_account_name = storage_account_name

        if self.storage_account:
            self.auth_mode = "storage_account_connection_string"
            self.client = self.storage_account.blob_service_client.get_blob_client(
                self.container, self.name
            )
        elif self.sas_url:
            self.auth_mode = "sas_url"
            self.client = BlobServiceClient(sas_url).get_blob_client(
                self.container, self.name
            )
        elif self.sas_key and self.storage_account_name:
            self.auth_mode = "sas_key"
            self.client = BlobServiceClient(
                "https://{}.blob.core.windows.net/{}".format(
                    self.storage_account_name, self.sas_key
                )
            ).get_blob_client(self.container, self.name)
        else:
            raise (BlobAthenticationFailedException(self.name))

    def get_sas_token(self):
        permission = BlobSasPermissions.from_string("racwd")

        self.sas_token = generate_blob_sas(
            self.storage_account.name,
            self.container,
            self.name,
            account_key=self.storage_account.key,
            permission=permission,
            expiry=datetime.utcnow() + timedelta(hours=1),
        )
        return self.sas_token

    def get_url(self):
        return "{}?{}".format(self.client.url, self.get_sas_token())

    def read(self):
        """read datas from blob
        
        :return: data read
        :rtype: binary string
        """
        return self.client.download_blob().readall()

    def read_csv(self, **kargs):
        """read CSV file from Blob

        Args:
            - path (string): remote csv file path to read
            - **kargs: arguments array passed to pandas.read_csv

        Returns:
            - pandas.DataFrame: DataFrame filled with read datas
        """

        return pd.read_csv(self.get_url(), **kargs)

    def gzip_write(self, data, overwrite=True):
        """write gzipped data to blob
        
        :param data: datas to write
        :type data: binary string
        :param overwrite: overwrite or not, defaults to True
        :type overwrite: bool, optional
        """
        return self.write(gzip.compress(data, compresslevel=9), overwrite=overwrite)

    def write(self, data, overwrite=True):
        return self.client.upload_blob(data, overwrite=overwrite)

    def upload(self, path, overwrite=True):
        """upload file to blob
        
        :param path: local path
        :type path: str
        :param overwrite: overwrite blob or not, defaults to True
        :type overwrite: bool, optional
        """
        with open(path, "rb") as data:
            self.write(data, overwrite=True)

    def download(self, path):
        with open(path, "wb") as data:
            data.write(self.read())

    def delete(self):
        return self.client.delete_blob()
