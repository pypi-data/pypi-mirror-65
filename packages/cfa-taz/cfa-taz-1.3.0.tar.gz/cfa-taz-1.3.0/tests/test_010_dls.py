#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from taz.dls import Datalake
import sys
import tests.config as cfg


class DatalakeTests(unittest.TestCase):

    def setUp(self):

        self.path = cfg.dls["path"]
        self.file_name = cfg.dls["file_name"]
        self.gz_file_name = cfg.dls["gz_file_name"]
        self.tmp_file_name = cfg.dls["tmp_file_name"]
        self.datalake = Datalake(
            cfg.dls["dls_name"],
            cfg.dls["tenant_id"],
            cfg.dls["client_id"],
            cfg.dls["client_secret"],
            proxy=cfg.dls["https_proxy"])

    def test_010_exists(self):
        self.assertTrue(self.datalake is not None)

    def test_020_df(self):
        stats = self.datalake.df(self.path)
        print("stats", stats)
        self.assertTrue(stats is not None)

    def test_030_ls(self):
        list_files = self.datalake.ls(self.path)
        print(list_files[0])
        self.assertTrue(list_files)

    def test_035_open(self):
        fd = self.datalake.open(self.path + '/' + self.file_name)
        fd.readline()
        fd.close()

    def test_040_copy(self):
        self.datalake.get(self.path + '/' + self.file_name, self.tmp_file_name)

    def test_050_read_csv(self):
        df = self.datalake.read_csv(
            self.path + '/' + self.file_name)
        self.assertTrue(df is not None)

    def test_050_read_gz_csv(self):
        df = self.datalake.read_csv(
            self.gz_file_name,
            compression="gzip")
        self.assertTrue(df is not None)


if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
