#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Taz library: Container Registry operations
"""

from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from msrestazure.azure_active_directory import MSIAuthentication
from azure.mgmt.containerinstance.models import ImageRegistryCredential

from azure.common.credentials import ServicePrincipalCredentials
import os


class ContainerRegistry:

    """Summary
    
    Attributes:
        - client (TYPE): Description
        - credentials (TYPE): Description
        - name (TYPE): Description
        - resource_group (TYPE): Description
    """

    def __init__(self, resource_group, name, subscription_id=None):

        self.tenant_id = os.environ.get("AZURE_TENANT_ID")
        self.client_id = os.environ.get("AZURE_CLIENT_ID")
        self.cli_user = os.environ.get("AZURE_CLI_USER")
        if subscription_id:
            self.subscription_id = subscription_id
        else:
            self.subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")

        if os.environ.get("AZURE_CLIENT_SECRET"):
            self.client = ContainerRegistryManagementClient(
                ServicePrincipalCredentials(
                    client_id=os.environ.get("AZURE_CLIENT_ID"),
                    secret=os.environ.get("AZURE_CLIENT_SECRET"),
                    tenant=os.environ.get("AZURE_TENANT_ID"),
                ),
                self.subscription_id,
            )
            self.mode = "service_principal"
        elif self.cli_user:
            print("cli profile")
            self.mode = "cli_profile"
            self.client = get_client_from_cli_profile(
                ContainerRegistryManagementClient, subscription_id=self.subscription_id
            )
        else:
            self.mode = "managed_identity"
            self.client = ContainerRegistryManagementClient(
                MSIAuthentication(), self.subscription_id
            )

        self.name = name
        self.resource_group = resource_group
        self.credentials = self.client.registries.list_credentials(resource_group, name)

    def get_credentials(self):
        return ImageRegistryCredential(
            server="{0}.azurecr.io".format(self.name),
            username=self.credentials.username,
            password=self.credentials.passwords[0].value,
        )


class ContainerImage:

    """Summary

    Attributes:
        container_registry (TYPE): Description
        name (TYPE): Description
    """

    def __init__(self, name, container_registry):

        self.container_registry = container_registry
        self.name = name

    def get_name(self):
        return self.name
