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

import json
import os
from azure.common.credentials import ServicePrincipalCredentials
from datetime import datetime

from taz.auth import UserAssignedIdentity, ClientSecretAuthentication, GenericClient
from taz.exception import ContainerAlreadyExistsException
from taz.blob import Blob


class SimpleContainerGroup:

    """Simplified Container Group with a Single container
    
    Attributes:
        - name (str): Description
        - generic_client (taz.auth.GenericClient): generic client to abstract authentication method
        - client (azure.mgmt.containerinstance.container_instance_management_client.ContainerInstanceManagementClient): 
          ACI management client provided by generic_client
        - command (list(str)): container entry point
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
        - state (string): state of container group 
        (Accessed if already created, Provisionned if it is prepared, and Created if it is created)
        - protected (bool): display env vars values or not
        - identity_name (str): name of user managed identity
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
        identity_name=None,
        identity=None,
        restart_policy="Never",
        env_vars=[],
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
            - command (None, list(str), optionnal): container entry point
            - identity (None, taz.auth.UserAssignedIdentity, optionnal): User managed identity to affect
            - restart_policy ("Never", str, optionnal): set restart policy of container
            - env_vars (None, dict, optionnal):  environment variables dictionnary to set
            - identity_name (None, str, optionnal): user managed identity by name (identity parameter ignored if set)
        """

        self.generic_client = GenericClient(
            ContainerInstanceManagementClient, subscription_id=subscription_id
        )
        self.client = self.generic_client.get_client()

        # Required parameters
        self.name = name
        self.resource_group_name = resource_group_name
        self.subscription_id = subscription_id

        # Optionnal parameters
        self.location = location
        self.image = image
        self.cpus = cpus
        self.mem = mem
        self.identity = identity
        self.restart_policy = restart_policy
        self.os_type = OperatingSystemTypes.linux
        self.command = command
        self.group = None
        self.instances = []
        self.tags = tags
        self.protected = True
        self.env_vars = []
        self.identity_name = identity_name
        self.container_name = "container-001"
        self.last_finish_time = None

        if env_vars:
            self.set_env_vars(env_vars)

        try:
            # container group already exists
            self._get_group()
            self.cpus = 0
            self.mem = 0
            self.state = "Accessed"
        except:

            # container group provisionned (before create methos call)
            self.state = "Provisionned"
            if self.identity_name:
                self.set_identity_by_name(self.identity_name)

    def _get_group(self):
        self.group = self.client.container_groups.get(
            self.resource_group_name, self.name
        )

        self.restart_policy = self.group.restart_policy
        self.identity = self.group.identity

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

    def set_env_vars(self, vars):
        """
        set env vars from dictionary
        
        Args:
            - vars (dict): env vars dictionary
        """
        for key, value in vars.items():
            self.add_env_var(key, value)

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

    def set_identity_by_name(self, identity_name, resource_group=None):
        """
        set identity by identity name instead of taz.auth.UserAssignedIdentity object (set_identity method)

        Args:
            - identity_name (str): user assigned identity name to affect
            - resource_group(None, str, optionnal): if not set, same as container group
        """
        if not resource_group:
            resource_group = self.resource_group_name
        self.identity_name = identity_name
        self.identity = UserAssignedIdentity(
            resource_group, self.identity_name, subscription_id=self.subscription_id
        ).get_container_group_identity()

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

        if self.state == "Accessed":
            raise (ContainerAlreadyExistsException(self.name))

        # Configure the container
        container_resource_requests = ResourceRequests(
            memory_in_gb=self.mem, cpu=self.cpus
        )
        container_resource_requirements = ResourceRequirements(
            requests=container_resource_requests
        )

        container = Container(
            name=self.container_name,
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
            tags=self.tags,
        )

        self.client.container_groups.create_or_update(
            self.resource_group_name, self.name, group
        )

        self._get_group()
        self.state = "Created"

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
        """list containers logs
        
        :return: return container logs
        :rtype: str
        """
        instances_logs = ""
        for instance in self.instances:
            instances_logs += "Logs for group '{}' for container '{}':\n".format(
                self.name, instance.name
            )
            try:
                instance_logs = self.client.container.list_logs(
                    self.resource_group_name, self.name, instance.name
                )
                instances_logs += "{0}".format(instance_logs.content) + "\n"
            except:
                instances_logs += "unavailable" + "\n"

        return instances_logs

    def save_logs(
        self,
        container,
        sas_url=None,
        sas_key=None,
        storage_account_name=None,
        storage_account=None,
    ):

        datas_group_logs = self.__str__()
        datas_container_logs = self.list_logs()

        if not self.last_finish_time == "None":
            name_group_log = "{}.{}.taz.aci.group.{}.log".format(
                self.last_start_time, self.last_finish_time, self.name
            )
            name_container_log = "{}.{}.taz.aci.container.{}.{}.log".format(
                self.last_start_time,
                self.last_finish_time,
                self.name,
                self.container_name,
            )
            blob_group_logs = Blob(
                container,
                name_group_log,
                sas_url=sas_url,
                sas_key=sas_key,
                storage_account_name=storage_account_name,
                storage_account=storage_account,
            )
            blob_container_logs = Blob(
                container,
                name_container_log,
                sas_url=sas_url,
                sas_key=sas_key,
                storage_account_name=storage_account_name,
                storage_account=storage_account,
            )
            blob_group_logs.write(datas_group_logs)
            blob_container_logs.write(datas_container_logs)

            return name_group_log, name_container_log
        else:
            return None

    def __str__(self):
        """
        prints container group as json string
        
        Returns:
            - str: json encoded as string
        """

        instances = []

        for instance in self.instances:
            events = []
            vars = []
            try:
                for var in instance.environment_variables:
                    if self.protected is False:
                        value = var.value
                    else:
                        value = "<protected>"
                    vars.append({var.name: value})
                for event in instance.instance_view.events:
                    events.append(
                        "{} {} {} {}".format(
                            event.first_timestamp,
                            event.last_timestamp,
                            event.name,
                            event.message,
                        )
                    )
                command = instance.command
                ports = instance.ports
                state = instance.instance_view.current_state.state
                start_time = str(instance.instance_view.current_state.start_time)
                finish_time = str(instance.instance_view.current_state.finish_time)
                self.last_finish_time = finish_time
                self.last_start_time = start_time
                exit_code = instance.instance_view.current_state.exit_code
                detail_status = instance.instance_view.current_state.detail_status
                memory = instance.resources.requests.memory_in_gb
                cpus = instance.resources.requests.cpu

            except:
                state = "unknown"
                start_time = "unknown"
                finish_time = "unknown"
                exit_code = "unknown"
                detail_status = "unknown"
                ports = []
                command = "unknown"
                cpus = "unknown"
                memory = "unknown"

            instances.append(
                {
                    "name": instance.name,
                    "image": instance.image,
                    "memory": memory,
                    "cpus": cpus,
                    "command": command,
                    "ports": ports,
                    "state": state,
                    "start_time": start_time,
                    "finish_time": finish_time,
                    "exit_code": exit_code,
                    "detail_status": detail_status,
                    "events": events,
                    "vars": vars,
                }
            )

        if self.group:
            group_name = self.group.name
        else:
            group_name = "None"

        return json.dumps(
            {
                "name": self.name,
                "identity": str(self.identity),
                "cpus": self.cpus,
                "memory": self.mem,
                "restart_policy": self.restart_policy,
                "state": self.state,
                "group_name": group_name,
                "instances": instances,
            },
            indent=4,
        )
