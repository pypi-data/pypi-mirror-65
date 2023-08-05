#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from taz.blob import StorageAccount, Blob, Container
import tests.config as cfg
import sys


class BlobTests(unittest.TestCase):

    def setUp(self):
        self.storage_account_name = cfg.blob["storage_account_name"]
        self.storage_key = cfg.blob["storage_key"]
        self.sas_key = cfg.blob["sas_key"]
        self.container_name = cfg.blob["container_name"]
        self.path = cfg.blob["path"]
        self.gzip_path = cfg.blob["gzip_path"]
        self.data = cfg.blob["data"]

    def test_010_get_storage_account(self):
        self.storage_account = StorageAccount(
            self.storage_account_name,
            self.storage_key)
        self.assertTrue(self.storage_account is not None)

    def test_012_get_container(self):
        self.test_010_get_storage_account()
        self.container = Container(self.storage_account, self.container_name)

    def test_015_create_container(self):
        self.test_012_get_container()
        self.container.create()

    def test_020_list_containers(self):
        self.test_010_get_storage_account()
        self.containers = self.storage_account.list_containers()
        for container in self.containers:
            print(container)
        self.assertTrue(self.containers is not None)

    def test_030_list_blobs(self):
        self.test_010_get_storage_account()
        self.blobs = self.storage_account.list_blobs(self.container_name)
        self.assertTrue(self.blobs is not None)

    def test_040_get_blob(self):
        self.test_010_get_storage_account()
        self.blob = Blob(
            self.storage_account,
            self.container_name,
            self.path,
            self.sas_key)
        self.assertTrue(self.blob is not None)

    def test_042_get_gzip_blob(self):
        self.test_010_get_storage_account()
        self.gzip_blob = Blob(
            self.storage_account,
            self.container_name,
            self.gzip_path,
            self.sas_key)
        self.assertTrue(self.gzip_blob is not None)

    def test_045_blob_write(self):
        self.test_040_get_blob()
        self.blob.write(self.path, bytes(self.data, 'utf-8'))

    def test_047_blob_gzip_write(self):
        self.test_042_get_gzip_blob()
        self.gzip_blob.gzip_write(self.gzip_path, bytes(self.data, 'utf-8'))

    def test_050_get_blob_sas_token(self):
        self.test_040_get_blob()
        self.sas_token = self.blob.get_sas_token()
        self.assertTrue(self.sas_token is not None)

    def test_060_get_blob_url(self):
        self.test_040_get_blob()
        self.url = self.blob.get_url()
        self.assertTrue(self.url is not None)

    def test_070_blob_read_raw(self):
        self.test_040_get_blob()
        self.assertTrue(self.blob.read() is not None)

    def test_080_blob_read_csv(self):
        self.test_040_get_blob()
        self.csv_datas = self.blob.read_csv()
        print(self.csv_datas)
        self.assertTrue(self.csv_datas is not None)

    def test_090_blob_read_gzip_csv(self):
        self.test_042_get_gzip_blob()
        self.csv_datas = self.gzip_blob.read_csv(compression="gzip")
        print(self.csv_datas)
        self.assertTrue(self.csv_datas is not None)

    def test_100_blob_delete(self):
        self.test_040_get_blob()
        self.blob.delete()

    def test_110_gzip_blob_delete(self):
        self.test_042_get_gzip_blob()
        self.gzip_blob.delete()

    def test_120_container_delete(self):
        self.test_012_get_container()
        self.container.delete()


if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
