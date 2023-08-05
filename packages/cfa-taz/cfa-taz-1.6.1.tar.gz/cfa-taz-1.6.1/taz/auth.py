#!/usr/bin/env python
# -*- coding: utf-8 -*-

from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.msi import ManagedServiceIdentityClient
from azure.mgmt.containerinstance.models import ContainerGroupIdentity
from msrestazure.azure_active_directory import MSIAuthentication
from azure.common.credentials import ServicePrincipalCredentials

import os
import json


class GenericClient:
    """Class GenericClient
    
    Attributes:
        - client_class (Class): Client class to build
        - tenant_id (string): Azure tenant id
        - subscription_id (string): Azure subscription id
        - client id (string): Azure client id
        - client_secret (string): Azure client secret
        - cli_profile (string): use cli profile if not None
        - mode (string): auth mode
            choice in this order:
            - cli_profile not None => cli profile authentication
            - client_secret not None => service principal authentication

    Environment variables:
        if corresponding attributes not set, read env vars:
        AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET and AZURE_CLI_PROFILE
    """

    def __init__(
        self,
        client_class,
        tenant_id=None,
        subscription_id=None,
        client_id=None,
        client_secret=None,
        cli_profile=None,
    ):
        """GenericClient Constructor
        
        :param client_class: client class to build
        :type client_class: class
        :param tenant_id: Azure tenant id, defaults to None
        :type tenant_id: string, optional
        :param subscription_id: Azure subscription id, defaults to None
        :type subscription_id: string, optional
        :param client_id: Azure client id, defaults to None
        :type client_id: string, optional
        :param client_secret: client secret, defaults to None
        :type client_secret: string, optional
        :param cli_profile: cli profile (None or else), defaults to None
        :type cli_profile: string, optional
        :return: Generic Azure Client Class
        :rtype: GenericClient
        """
        self.client_class = client_class

        if tenant_id:
            self.tenant_id = tenant_id
        else:
            self.tenant_id = os.environ.get("AZURE_TENANT_ID")

        if subscription_id:
            self.subscription_id = subscription_id
        else:
            self.subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")

        if client_id:
            self.client_id = client_id
        else:
            self.client_id = os.environ.get("AZURE_CLIENT_ID")

        if client_secret:
            self.client_secret = client_secret
        else:
            self.client_secret = os.environ.get("AZURE_CLIENT_SECRET")

        if cli_profile:
            self.cli_profile = cli_profile
        else:
            self.cli_profile = os.environ.get("AZURE_CLI_PROFILE")

        if self.cli_profile:
            self.mode = "cli_profile"
        elif self.client_secret:
            self.mode = "service_principal"
        else:
            self.mode = "msi"

    def get_client(self):
        """get Azure Client class
        
        :return: Azure Client Class
        :rtype: class
        """
        if self.mode == "service_principal":
            self.client = self.client_class(
                ServicePrincipalCredentials(
                    client_id=self.client_id,
                    secret=self.client_secret,
                    tenant=self.tenant_id,
                ),
                subscription_id=self.subscription_id,
            )
            return self.client
        elif self.mode == "cli_profile":
            self.client = get_client_from_cli_profile(
                self.client_class, subscription_id=self.subscription_id
            )
            return self.client
        else:
            self.client = self.client_class(
                MsiAuthentication(), subscription_id=self.subscription_id
            )
            return self.client


class UserAssignedIdentity:

    """User Assigned identity
    
    Attributes:
        - client (ManagedServiceIdentityClient): MSI client
        - container_group_identity (ContainerGroupIdentity): identity to use
        with container group
        - identity (TYPE): Description
        - managed_identity_name (TYPE): Description
        - resource_group_name (string): Resource Group
        - subscription_id (string): subscription id
    """

    def __init__(
        self, resource_group_name, managed_identity_name, subscription_id=None
    ):
        """
        Create a user assigned identity object

        Args:
            resource_group (string): resource group name
            managed_identity (string): managed identity name
            subscription_id (None, optional): subscription id (if None default)
        """

        generic_client = GenericClient(
            ManagedServiceIdentityClient, subscription_id=subscription_id
        )
        self.client = generic_client.get_client()

        self.subscription_id = subscription_id
        self.resource_group_name = resource_group_name
        self.managed_identity_name = managed_identity_name
        self.identity = self.get_identity()

    def get_identity(self):
        self.identity = self.client.user_assigned_identities.get(
            self.resource_group_name, self.managed_identity_name
        )

        return self.identity

    def get_container_group_identity(self):
        self.get_identity()

        self.container_group_identity = ContainerGroupIdentity(
            type="UserAssigned", user_assigned_identities={self.identity.id: {}}
        )
        return self.container_group_identity

    def __str__(self):
        return json.dumps(
            {
                "id": self.identity.id,
                "name": self.identity.name,
                "tenant_id": self.identity.tenant_id,
                "principal_id": self.identity.principal_id,
                "client_id": self.identity.client_id,
                "type": self.identity.type,
            },
            indent=4,
        )


class MsiAuthentication:
    def __init__(self):
        self.credentials = MSIAuthentication()

    def get_credentials(self):
        return self.credentials


class ClientSecretAuthentication:
    def __init__(
        self, tenant_id=None, subscription_id=None, client_id=None, client_secret=None
    ):
        """Client/Client secret authentication
        
        :param tenant_id: tenant_id or AZURE_TENANT_ID env var, defaults to None
        :type tenant_id: string, optional
        :param subscription_id: subscription_id or AZURE_SUBSCRIPTION_ID env var, defaults to None
        :type subscription_id: string, optional
        :param client_id: client_id or AZURE_CLIENT_ID env var, defaults to None
        :type client_id: string, optional
        :param client_secret: client_secret or AZURE_CLIENT_SECRET env var, defaults to None
        :type client_secret: string, optional
        """
        if tenant_id is None:
            self.tenant_id = os.environ.get("AZURE_TENANT_ID")
        else:
            self.tenant_id = tenant_id

        if subscription_id is None:
            self.subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
        else:
            self.subscription_id = subscription_id

        if client_id is None:
            self.client_id = os.environ.get("AZURE_CLIENT_ID")
        else:
            self.client_id = client_id

        if client_secret is None:
            self.client_secret = os.environ.get("AZURE_CLIENT_SECRET")
        else:
            self.client_secret = client_secret

        self.credentials = ServicePrincipalCredentials(
            tenant=self.tenant_id, client_id=self.client_id, secret=self.client_secret
        )

    def get_credentials(self):
        return self.credentials
