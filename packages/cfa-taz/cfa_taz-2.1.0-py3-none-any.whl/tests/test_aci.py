#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from taz.aci import SimpleContainerGroup
from taz.acr import ContainerRegistry
from taz.acr import ContainerImage
import tests.config as cfg
import sys


class AciTests(unittest.TestCase):
    def setUp(self):

        self.container_registry = ContainerRegistry(
            cfg.acr["resource_group"],
            cfg.acr["registry_name"],
            subscription_id=cfg.acr["subscription_id"],
        )

        self.container_image = ContainerImage(
            cfg.acr["image_name"], self.container_registry
        )

        self.container_group = SimpleContainerGroup(
            cfg.aci["container_group_name"],
            cfg.aci["resource_group"],
            cfg.aci["location"],
            self.container_image,
            subscription_id=cfg.aci["subscription_id"],
        )

    def test_01_exists(self):
        self.assertTrue(self.container_registry is not None)
        self.assertTrue(self.container_image is not None)
        self.assertTrue(self.container_group is not None)
        print(self.container_group)

    def test_02_create(self):
        self.container_group.create()
        self.assertTrue(self.container_group.get_group() is not None)
        self.assertTrue(len(self.container_group.instances) == 1)
        print(self.container_group.generic_client.mode)
        print(self.container_group)

    def test_03_delete(self):
        self.container_group.delete()


if __name__ == "__main__":
    sys.argv.append("-v")
    unittest.main()
