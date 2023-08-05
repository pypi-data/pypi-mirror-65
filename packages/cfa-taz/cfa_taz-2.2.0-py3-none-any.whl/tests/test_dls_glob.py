#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from taz.dls import Datalake
import sys
import tests.config as cfg


class DatalakeTests(unittest.TestCase):

    def setUp(self):

        self.path = cfg.dls["path"]
        self.glob_path = cfg.dls["glob_path"]
        self.file_name = cfg.dls["file_name"]
        self.gz_file_name = cfg.dls["gz_file_name"]
        self.tmp_file_name = cfg.dls["tmp_file_name"]
        self.datalake = Datalake(
            cfg.dls["dls_name"],
            cfg.dls["tenant_id"],
            cfg.dls["client_id"],
            cfg.dls["client_secret"],
            proxy=cfg.dls["https_proxy"])

    def test_020_glob(self):
        list_files = self.datalake.glob(self.glob_path)
        print(list_files)
        self.assertTrue(list_files)


if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
