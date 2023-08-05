#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from taz.aci import SimpleContainerGroup
from taz.acr import ContainerRegistry
from taz.acr import ContainerImage
import tests.config as cfg
import sys


class AciViewTests(unittest.TestCase):
    def setUp(self):

        self.container_group = SimpleContainerGroup(
            cfg.aci["container_group_name"], cfg.aci["resource_group"],
        )
        self.logs_sas_key = cfg.aci["logs_sas_key"]
        self.logs_container = cfg.aci["logs_container"]
        self.logs_storage_account = cfg.aci["logs_storage_account"]

    def test_10_display(self):
        self.assertTrue(self.container_group is not None)
        print(self.container_group)

    def test_15_display_unprotected(self):
        self.assertTrue(self.container_group is not None)
        self.container_group.protected = False
        print(self.container_group)

    def test_20_list_logs(self):
        print(self.container_group.list_logs())

    def test_30_save_logs(self):
        print(
            self.container_group.save_logs(
                self.logs_container,
                sas_key=self.logs_sas_key,
                storage_account_name=self.logs_storage_account,
            )
        )


if __name__ == "__main__":
    sys.argv.append("-v")
    unittest.main()
