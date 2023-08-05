#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ContainerAlreadyExistsException(Exception):
    def __init__(self, container_name):
        self.container_name = container_name


class BlobAthenticationFailedException(Exception):
    def __init__(self, blob_name):
        self.blob_name = blob_name
