#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from taz.acr import ContainerRegistry
from taz.acr import ContainerImage
import tests.config as cfg
import sys


class AcrTests(unittest.TestCase):
    def setUp(self):
        self.container_registry = ContainerRegistry(
            cfg.acr["resource_group"],
            cfg.acr["registry_name"],
            subscription_id=cfg.acr["subscription_id"],
        )

        self.container_image = ContainerImage(
            cfg.acr["image_name"], self.container_registry
        )

    def test_exists(self):
        print(self.container_registry.mode)
        self.assertTrue(self.container_registry is not None)
        self.assertTrue(self.container_image is not None)

    def test_get_credentials(self):
        self.assertTrue(self.container_registry.get_credentials() is not None)


if __name__ == "__main__":
    sys.argv.append("-v")
    unittest.main()
