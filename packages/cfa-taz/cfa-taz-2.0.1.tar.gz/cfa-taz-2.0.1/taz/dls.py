#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
from azure.datalake.store import core, lib
from adal.adal_error import AdalError


class Datalake:
    def __init__(
        self,
        name,
        tenant_id,
        client_id,
        secret,
        proxy=None
    ):
        """
        Datalake connection

        Args:
            - name (string): Datalake name
            - tenant_id (string): Azure tenant id
            - client_id (string): service principal client id
            - secret (TYPE): service principal password
            - proxy (None, optional): HTTPS proxy
        """

        if proxy is not None:
            self.proxy = proxy
            os.environ['https_proxy'] = proxy

        try:
            self.token = lib.auth(
                tenant_id=tenant_id,
                client_secret=secret,
                client_id=client_id,
                resource='https://management.core.windows.net/')
        except AdalError as error:
            raise error

        self.conn = core.AzureDLFileSystem(
            self.token,
            store_name=name)

    def ls(self, path):
        """list DLS path
        
        Args:
            - path (string): path to list
        
        Returns:
            - (list) of dictionnaries: node entry metadatas with folowing keys:
                - 'length'
                - 'pathSuffix'
                - 'type'
                - 'blockSize'
                - 'accessTime'
                - 'modificationTime'
                - 'replication'
                - 'permission'
                - 'owner'
                - 'group'
                - 'msExpirationTime'
                - 'aclBit'
                - 'name'
        """
        return self.conn.ls(path, detail=True)

    def glob(self, path, details=True):
        """list DLS path with globbing
        
        Args:
            - path (string): path to list
        
        Returns:
            - (list) of dictionnaries: node entry metadatas with folowing keys:
                - 'length'
                - 'pathSuffix'
                - 'type'
                - 'blockSize'
                - 'accessTime'
                - 'modificationTime'
                - 'replication'
                - 'permission'
                - 'owner'
                - 'group'
                - 'msExpirationTime'
                - 'aclBit'
                - 'name'
        """
        return self.conn.glob(path, details=True)

    def get(self, srcpath, destpath):
        """download file from Datalake
        
        Args:
            srcpath (string): source path
            destpath (string): local destination path
        
        Returns:
            TYPE: Description
        """
        return self.conn.get(srcpath, destpath)

    def open(self, path):
        """open a stream descriptor on remote file
        
        Args:
            path (string): file path to open
        
        Returns:
            azure.datalake.store.core.AzureDLFile: Description
        """
        return self.conn.open(path)

    def read_csv(self, path, **kargs):
        """read CSV file from Datalake
        
        Args:
            - path (string): remote csv file path to read
            - **kargs: arguments array passed to pandas.read_csv
        
        Returns:
            - pandas.DataFrame: DataFrame filled with read datas
        """
        fd = self.open(path)
        df = pd.read_csv(fd, **kargs)
        fd.close()
        return df

    def df(self, path):
        """describe 
        
        Args:
            path (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        stats = self.conn.df(path)
        return list(
            [
                stats['directoryCount'],
                stats['fileCount'],
                stats['spaceConsumed'] / 1024 / 1024 / 1024
            ])
