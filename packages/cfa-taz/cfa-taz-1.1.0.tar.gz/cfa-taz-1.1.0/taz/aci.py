#!/usr/bin/env python
# -*- coding: utf-8 -*-

from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from taz.acr import ContainerRegistry
from msrestazure.azure_active_directory import MSIAuthentication
from azure.mgmt.containerinstance.container_instance_management_client import (
    ContainerInstanceManagementClient,
)

from azure.mgmt.containerinstance.models import (
    ContainerGroup,
    Container,
    ContainerGroupNetworkProtocol,
    ContainerPort,
    EnvironmentVariable,
    IpAddress,
    Port,
    ResourceRequests,
    ResourceRequirements,
    OperatingSystemTypes,
)

from taz.auth import UserAssignedIdentity, ClientSecretAuthentication, GenericClient
import json
import os
from azure.common.credentials import ServicePrincipalCredentials


class SimpleContainerGroup:

    """Summary
    
    Attributes:
        - name (str): Description
        - generic_client (taz.auth.GenericClient): generic client to abstract authentication method
        - client (azure.mgmt.containerinstance.container_instance_management_client.ContainerInstanceManagementClient): 
          ACI management client provided by generic_client
        - command (string): container entry point
        - cpus (int): vcpus for all container group (1-4 for northeurope 2020/03)
        - env_vars (list[azure.mgmt.containerinstance.models.EnvironmentVariable]): container environment variables
        - group (ContainerGroup): container group
        - identity (taz.auth.UserAssignedIdentity): user managed identity
        - image (taz.acr.ContainerImage): docker image to use
        - instances (list[azure.mgmt.containeris-nstance.Container]): Container instances in container group
        - location (str): Azure location
        - mem (int): memory for all container group (1-14GB for northeurope 2020/03)
        - os_type (constant, str): set to OperatingSystemTypes.linux
        - resource_group_name (str): resource group
        - restart_policy (str): Always/OnFailure/Never
        - tags (dict[str, str]): Azure tags
    """

    def __init__(
        self,
        name,
        resource_group_name,
        location="northeurope",
        image=None,
        subscription_id=None,
        tags=None,
        cpus=1,
        mem=1,
        command=None,
        identity=None,
        restart_policy="Never",
    ):
        """
        Simple container group object with one instance
        
        Args:
            - name (str): container group name
            - resource_group_name (str): resource group
            - location ("northeurope", str, optionnal): location
            - image (None, taz.acr.ContainerImage, optionnal): ContainerImage object (if no image, get existing container group)
            - subscription_id (None, optional, str): subscription id
            - tags (None, optionnal, dict[str, str]): tags 
            - cpus (1, int, optionnal): vcpus for all container group (1-4 for northeurope 2020/03)
            - mem (1, int, optionnal): memory for all container group (1-14GB for northeurope 2020/03)
            - command (None, str, optionnal): container entry point
            - identity (None, taz.auth.UserAssignedIdentity, optionnal): User managed identity to affect
            - restart_policy ("Never", str, optionnal): set restart policy of container
        """

        self.generic_client = GenericClient(
            ContainerInstanceManagementClient, subscription_id=subscription_id
        )
        self.client = self.generic_client.get_client()

        # Required parameters
        self.name = name
        self.resource_group_name = resource_group_name

        # Optionnal parameters
        self.location = location
        self.image = image
        self.cpus = cpus
        self.mem = mem
        self.env_vars = []
        self.identity = identity
        self.restart_policy = restart_policy
        self.os_type = OperatingSystemTypes.linux
        self.command = command
        self.group = None
        self.instances = []
        self.tags = tags

        if not self.image:
            self._get_group()

    def _get_group(self):
        self.group = self.client.container_groups.get(
            self.resource_group_name, self.name
        )
        for instance in self.group.containers:
            self.instances.append(instance)

    def add_env_var(self, name, value):
        """
        add environement var
        
        Args:
            - name (str): env var name
            - value (str): env var value
        """
        self.env_vars.append(EnvironmentVariable(name=name, value=value))

    def set_cpus(self, cpus):
        """
        set cores number
        
        Args:
            - cpus (int): 1-4 (actual limit for northeurope)
        """
        self.cpus = cpus

    def set_mem(self, mem):
        """
        set amount of memory in GB
        
        Args:
            - mem (int): 1-14 (actual limit for northeurope)
        """
        self.mem = mem

    def set_identity(self, identity):
        """
        set user managed identity
        
        Args:
            - identity (taz.auth.UserAssignedIdentity): container group identity
        """
        self.identity = identity.get_container_group_identity()

    def set_command(self, command):
        """
        set command entry point of container
        
        Args:
            - command (str): entry point script of container
        """
        self.command = command

    def create(self):
        """
        Create the container group and instance
        """

        # Configure the container
        container_resource_requests = ResourceRequests(
            memory_in_gb=self.mem, cpu=self.cpus
        )
        container_resource_requirements = ResourceRequirements(
            requests=container_resource_requests
        )

        container = Container(
            name="container-001",
            image="{0}.azurecr.io/{1}:latest".format(
                self.image.container_registry.name, self.image.name
            ),
            resources=container_resource_requirements,
            environment_variables=self.env_vars,
            command=self.command,
        )

        group = ContainerGroup(
            location=self.location,
            containers=[container],
            os_type=self.os_type,
            restart_policy=self.restart_policy,
            image_registry_credentials=[
                self.image.container_registry.get_credentials()
            ],
            identity=self.identity,
        )

        self.client.container_groups.create_or_update(
            self.resource_group_name, self.name, group
        )

        self._get_group()

    def get_group(self):
        """
        Return container group attribute
        
        Returns:
            - azure.mgmt.containerinstance.models.ContainerGroup: container 
                group object
        """
        return self.group

    def get_instances(self):
        """
        Summary
        
        Returns:
            - [ azure.mgmt.containerinstance.models.Container ]: List of
                container instances
        """
        return self.instances

    def delete(self):
        """
        delete container group and his containers
        """
        self.client.container_groups.delete(self.resource_group_name, self.name)

    def list_logs(self):
        instances_logs = ""
        for instance in self.instances:
            instances_logs += "Logs for group '{}' for container '{}':\n".format(
                self.name, instance.name
            )
            instance_logs = self.client.container.list_logs(
                self.resource_group_name, self.name, instance.name
            )
            instances_logs += instance_logs.content + "\n"
            try:
                instance_logs = self.client.container.list_logs(
                    self.resource_group_name, self.name, instance.name
                )
                instances_logs += "{0}".format(instance_logs.content) + "\n"
            except:
                instances_logs += "unavailable" + "\n"

        return instances_logs

    def __str__(self):
        """
        prints container group as json string
        
        Returns:
            - str: json encoded as string
        """

        instances = []

        for instance in self.instances:
            try:
                state = instance.instance_view.current_state.state
            except:
                state = "unknown"
            instances.append(
                {"name": instance.name, "image": instance.image, "state": state}
            )

        if self.group:
            group_name = self.group.name
        else:
            group_name = "None"

        return json.dumps(
            {
                "name": self.name,
                "cpus": self.cpus,
                "mem": self.mem,
                "restart_policy": self.restart_policy,
                "command": self.command,
                "instances": instances,
                "group_name": group_name,
            }
        )
