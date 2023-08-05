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

    def test_10_display(self):
        self.assertTrue(self.container_group is not None)
        print(self.container_group)

    def test_15_display_unprotected(self):
        self.assertTrue(self.container_group is not None)
        self.container_group.protected = False
        print(self.container_group)

    def test_20_list_logs(self):
        print(self.container_group.list_logs())


if __name__ == "__main__":
    sys.argv.append("-v")
    unittest.main()
