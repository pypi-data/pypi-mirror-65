#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from taz.keyvault import KeyVault
import tests.config as cfg
import sys
import os


class KeyvaultTests(unittest.TestCase):

    def setUp(self):
        os.environ["AZURE_TENANT_ID"] = cfg.keyvault['tenant_id']
        os.environ["AZURE_CLIENT_ID"] = cfg.keyvault['client_id']
        os.environ["AZURE_CLIENT_SECRET"] = cfg.keyvault['client_secret']

        self.keyvault = KeyVault(cfg.keyvault['name'])
        print(self.keyvault.mode)

    def test_01_exists(self):
        self.assertTrue(self.keyvault is not None)

    def test_10_get_mode(self):
        self.assertTrue(
            self.keyvault.mode == "service_principal")

    def test_20_get_secret(self):
        secret = self.keyvault.get_secret(cfg.keyvault['secret_name'], '')
        self.assertTrue(secret is not None)

    def test_30_set_secret(self):
        self.keyvault.set_secret('testtazkey', 'testtazvalue')

    def test_40_get_secret(self):
        self.assertTrue(
            self.keyvault.get_secret('testtazkey').value == "testtazvalue")



if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
