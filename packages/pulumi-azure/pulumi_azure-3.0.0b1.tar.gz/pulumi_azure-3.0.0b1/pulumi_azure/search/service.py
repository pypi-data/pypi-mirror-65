# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Service(pulumi.CustomResource):
    location: pulumi.Output[str]
    """
    The Azure Region where the Search Service should exist. Changing this forces a new Search Service to be created.
    """
    name: pulumi.Output[str]
    """
    The Name which should be used for this Search Service. Changing this forces a new Search Service to be created.
    """
    partition_count: pulumi.Output[float]
    """
    The number of partitions which should be created.
    """
    primary_key: pulumi.Output[str]
    """
    The Primary Key used for Search Service Administration.
    """
    query_keys: pulumi.Output[list]
    """
    A `query_keys` block as defined below.

      * `key` (`str`) - The value of this Query Key.
      * `name` (`str`) - The Name which should be used for this Search Service. Changing this forces a new Search Service to be created.
    """
    replica_count: pulumi.Output[float]
    """
    The number of replica's which should be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the Resource Group where the Search Service should exist. Changing this forces a new Search Service to be created.
    """
    secondary_key: pulumi.Output[str]
    """
    The Secondary Key used for Search Service Administration.
    """
    sku: pulumi.Output[str]
    """
    The SKU which should be used for this Search Service. Possible values are `basic`, `free`, `standard`, `standard2` and `standard3` Changing this forces a new Search Service to be created.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags which should be assigned to the Search Service.
    """
    def __init__(__self__, resource_name, opts=None, location=None, name=None, partition_count=None, replica_count=None, resource_group_name=None, sku=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a Search Service.



        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/search_service.html.markdown.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The Azure Region where the Search Service should exist. Changing this forces a new Search Service to be created.
        :param pulumi.Input[str] name: The Name which should be used for this Search Service. Changing this forces a new Search Service to be created.
        :param pulumi.Input[float] partition_count: The number of partitions which should be created.
        :param pulumi.Input[float] replica_count: The number of replica's which should be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Search Service should exist. Changing this forces a new Search Service to be created.
        :param pulumi.Input[str] sku: The SKU which should be used for this Search Service. Possible values are `basic`, `free`, `standard`, `standard2` and `standard3` Changing this forces a new Search Service to be created.
        :param pulumi.Input[dict] tags: A mapping of tags which should be assigned to the Search Service.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['location'] = location
            __props__['name'] = name
            __props__['partition_count'] = partition_count
            __props__['replica_count'] = replica_count
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if sku is None:
                raise TypeError("Missing required property 'sku'")
            __props__['sku'] = sku
            __props__['tags'] = tags
            __props__['primary_key'] = None
            __props__['query_keys'] = None
            __props__['secondary_key'] = None
        super(Service, __self__).__init__(
            'azure:search/service:Service',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, location=None, name=None, partition_count=None, primary_key=None, query_keys=None, replica_count=None, resource_group_name=None, secondary_key=None, sku=None, tags=None):
        """
        Get an existing Service resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The Azure Region where the Search Service should exist. Changing this forces a new Search Service to be created.
        :param pulumi.Input[str] name: The Name which should be used for this Search Service. Changing this forces a new Search Service to be created.
        :param pulumi.Input[float] partition_count: The number of partitions which should be created.
        :param pulumi.Input[str] primary_key: The Primary Key used for Search Service Administration.
        :param pulumi.Input[list] query_keys: A `query_keys` block as defined below.
        :param pulumi.Input[float] replica_count: The number of replica's which should be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Search Service should exist. Changing this forces a new Search Service to be created.
        :param pulumi.Input[str] secondary_key: The Secondary Key used for Search Service Administration.
        :param pulumi.Input[str] sku: The SKU which should be used for this Search Service. Possible values are `basic`, `free`, `standard`, `standard2` and `standard3` Changing this forces a new Search Service to be created.
        :param pulumi.Input[dict] tags: A mapping of tags which should be assigned to the Search Service.

        The **query_keys** object supports the following:

          * `key` (`pulumi.Input[str]`) - The value of this Query Key.
          * `name` (`pulumi.Input[str]`) - The Name which should be used for this Search Service. Changing this forces a new Search Service to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["location"] = location
        __props__["name"] = name
        __props__["partition_count"] = partition_count
        __props__["primary_key"] = primary_key
        __props__["query_keys"] = query_keys
        __props__["replica_count"] = replica_count
        __props__["resource_group_name"] = resource_group_name
        __props__["secondary_key"] = secondary_key
        __props__["sku"] = sku
        __props__["tags"] = tags
        return Service(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

