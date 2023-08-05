#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from taz.auth import UserAssignedIdentity, ClientSecretAuthentication, GenericClient
from azure.mgmt.msi import ManagedServiceIdentityClient

import sys
import os
import tests.config as cfg


class AuthTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_01_exists(self):
        self.user_assigned_identity = UserAssignedIdentity(
            cfg.auth["resource_group"],
            cfg.auth["managed_identity"],
            subscription_id=cfg.auth["subscription_id"],
        )
        self.assertTrue(self.user_assigned_identity is not None)

    def test_02_secret_credentials_by_params(self):
        self.client_secret_credentials = ClientSecretAuthentication(
            cfg.auth["tenant_id"],
            cfg.auth["subscription_id"],
            cfg.auth["client_id"],
            cfg.auth["client_secret"],
        )
        print(self.client_secret_credentials.get_credentials())

    def test_03_secret_credentials_by_env(self):
        os.environ["AZURE_TENANT_ID"] = cfg.auth["tenant_id"]
        os.environ["AZURE_SUBSCRIPTION_ID"] = cfg.auth["subscription_id"]
        os.environ["AZURE_CLIENT_ID"] = cfg.auth["client_id"]
        os.environ["AZURE_CLIENT_SECRET"] = cfg.auth["client_secret"]

        self.client_secret_credentials = ClientSecretAuthentication()
        print(self.client_secret_credentials.get_credentials())

    def test_04_container_group_identity(self):
        self.user_assigned_identity = UserAssignedIdentity(
            cfg.auth["resource_group"],
            cfg.auth["managed_identity"],
            subscription_id=cfg.auth["subscription_id"],
        )
        self.assertTrue(
            self.user_assigned_identity.get_container_group_identity() is not None
        )

    def test_05_managed_identity(self):
        self.user_assigned_identity = UserAssignedIdentity(
            cfg.auth["resource_group"],
            cfg.auth["managed_identity"],
            subscription_id=cfg.auth["subscription_id"],
        )
        self.assertTrue(self.user_assigned_identity is not None)

    def test_06_generic_client_by_sp(self):
        self.generic_client = GenericClient(ManagedServiceIdentityClient)
        self.assertTrue(self.generic_client is not None)
        print("test_aci:", self.generic_client.mode)

    def test_07_generic_client_by_cli_param(self):
        self.generic_client = GenericClient(
            ManagedServiceIdentityClient, cli_profile="yes"
        )
        self.assertTrue(self.generic_client is not None)
        print("test_aci:", self.generic_client.mode)

    def test_08_generic_client_by_cli_env(self):
        os.environ["AZURE_CLI_PROFILE"] = "yes"
        self.generic_client = GenericClient(ManagedServiceIdentityClient)
        self.assertTrue(self.generic_client is not None)
        print("test_aci:", self.generic_client.mode)


if __name__ == "__main__":
    sys.argv.append("-v")
    unittest.main()
