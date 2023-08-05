#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from taz.aci import SimpleContainerGroup
from taz.acr import ContainerRegistry
from taz.acr import ContainerImage
from taz.auth import UserAssignedIdentity
import tests.config as cfg
import sys

from azure.mgmt.containerinstance.models import EnvironmentVariable


class AciCreateTests(unittest.TestCase):
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
            env_vars={"APPHOME1": "/home/app1"},
            tags={"APP": "WAG"},
        )

    def test_10_exists(self):
        self.assertTrue(self.container_registry is not None)
        self.assertTrue(self.container_image is not None)
        self.assertTrue(self.container_group is not None)
        print(self.container_group)

    def test_15_env_var(self):
        self.container_group.add_env_var("APPHOME2", "/home/app2")
        print(self.container_group)
        self.assertEqual(len(self.container_group.env_vars), 2)

    def test_20_create(self):
        self.container_group.create()
        self.assertTrue(self.container_group.get_group() is not None)
        self.assertTrue(len(self.container_group.instances) == 1)
        print(self.container_group.generic_client.mode)
        print(self.container_group)

    def test_22_user_assigned_identity(self):
        self.container_group.set_identity(
            UserAssignedIdentity(
                cfg.aci["resource_group"],
                "mi-aci-wag-dev-01",
                subscription_id=cfg.aci["subscription_id"],
            )
        )
        print(self.container_group)

    def test_25_print_group(self):
        print(self.container_group)


if __name__ == "__main__":
    sys.argv.append("-v")
    unittest.main()
