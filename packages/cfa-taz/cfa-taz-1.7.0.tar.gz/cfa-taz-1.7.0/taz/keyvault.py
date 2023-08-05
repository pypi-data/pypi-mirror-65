#!/usr/bin/env python
# -*- coding: utf-8 -*-

from azure.keyvault.secrets import SecretClient
from azure.identity import (
    DefaultAzureCredential,
    ChainedTokenCredential,
    ClientSecretCredential,
    ManagedIdentityCredential,
    InteractiveBrowserCredential,
)
import os


class KeyVault:

    """create keyvault object azure.keyvault.secrets

    parameters:
        - name: keyvault name

    attributes:
        - client (azure.keyvault.secrets.SecretClient): Azure Secrets Keyvault client
        - name (string): keyvault name
        - mode (string): connection mode based on environment vars
        AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET and AZURE_CLI_USER
            - service_proicipal: service principal authentication if AZURE_CLIENT_SECRET is set
            - cli_profile: CLI based authentication if AZURE_CLI_USER var is set
            - msi: MSI otherwise
    """

    def __init__(self, name):
        self.name = name

        self.tenant_id = os.environ.get("AZURE_TENANT_ID")
        self.client_id = os.environ.get("AZURE_CLIENT_ID")
        self.cli_user = os.environ.get("AZURE_CLI_USER")

        if os.environ.get("AZURE_CLIENT_SECRET"):
            credentials = self._get_sp_credentials(
                self.tenant_id, self.client_id, os.environ.get("AZURE_CLIENT_SECRET")
            )
        elif self.client_id:
            credentials = self._get_user_msi_credentials(self.client_id)
        elif self.cli_user:
            credentials = self._get_cli_profile_credentials()
        else:
            credentials = self._get_system_msi_credentials()

        self.client = SecretClient(
            "https://{}.vault.azure.net/".format(self.name), credentials
        )

    def _get_cli_profile_credentials(self):
        self.mode = "cli_profile"
        return InteractiveBrowserCredential()

    def _get_system_msi_credentials(self):
        self.mode = "system_msi"
        return ManagedIdentityCredential()

    def _get_user_msi_credentials(self, client_id):
        self.mode = "user_msi"
        return ManagedIdentityCredential(client_id=client_id)

    def _get_sp_credentials(self, tenant_id, client_id, client_secret):
        self.mode = "service_principal"
        return ClientSecretCredential(tenant_id, client_id, client_secret)

    def get_secret(self, secret_id, secret_version=""):
        """
        get secret value of a specified secret

        parameters:
            - secret_id: name or url of the secret
            - secret_version: version to retrieve

        return:
            -  azure.keyvault.secrets.Secret object
                - value: secret value
                - SecretProperties: secret metadatas (azure.keyvault.secrets.SecretProperties object)
        """

        return self.client.get_secret(secret_id, secret_version)

    def set_secret(self, secret_id, value):
        """
        set secret specified

        parameters:
            - secret_id: name of secret to set
            - value: secret value to set

        return:
            - none
        """
        self.client.set_secret(secret_id, value)
