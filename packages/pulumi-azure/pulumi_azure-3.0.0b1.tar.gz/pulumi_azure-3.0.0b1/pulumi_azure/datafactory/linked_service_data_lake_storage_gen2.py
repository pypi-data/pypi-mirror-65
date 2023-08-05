# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class LinkedServiceDataLakeStorageGen2(pulumi.CustomResource):
    additional_properties: pulumi.Output[dict]
    """
    A map of additional properties to associate with the Data Factory Linked Service MySQL.
    """
    annotations: pulumi.Output[list]
    """
    List of tags that can be used for describing the Data Factory Linked Service MySQL.
    """
    data_factory_name: pulumi.Output[str]
    """
    The Data Factory name in which to associate the Linked Service with. Changing this forces a new resource.
    """
    description: pulumi.Output[str]
    """
    The description for the Data Factory Linked Service MySQL.
    """
    integration_runtime_name: pulumi.Output[str]
    """
    The integration runtime reference to associate with the Data Factory Linked Service MySQL.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the Data Factory Linked Service MySQL. Changing this forces a new resource to be created. Must be globally unique. See the [Microsoft documentation](https://docs.microsoft.com/en-us/azure/data-factory/naming-rules) for all restrictions.
    """
    parameters: pulumi.Output[dict]
    """
    A map of parameters to associate with the Data Factory Linked Service MySQL.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which to create the Data Factory Linked Service MySQL. Changing this forces a new resource
    """
    service_principal_id: pulumi.Output[str]
    """
    The service principal id in which to authenticate against the Azure Data Lake Storage Gen2 account.
    """
    service_principal_key: pulumi.Output[str]
    """
    The service principal key in which to authenticate against the Azure Data Lake Storage Gen2 account.
    """
    tenant: pulumi.Output[str]
    """
    The tenant id or name in which to authenticate against the Azure Data Lake Storage Gen2 account.
    """
    url: pulumi.Output[str]
    """
    The endpoint for the Azure Data Lake Storage Gen2 service.
    """
    def __init__(__self__, resource_name, opts=None, additional_properties=None, annotations=None, data_factory_name=None, description=None, integration_runtime_name=None, name=None, parameters=None, resource_group_name=None, service_principal_id=None, service_principal_key=None, tenant=None, url=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a Linked Service (connection) between Data Lake Storage Gen2 and Azure Data Factory.



        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/data_factory_linked_service_data_lake_storage_gen2.html.markdown.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] additional_properties: A map of additional properties to associate with the Data Factory Linked Service MySQL.
        :param pulumi.Input[list] annotations: List of tags that can be used for describing the Data Factory Linked Service MySQL.
        :param pulumi.Input[str] data_factory_name: The Data Factory name in which to associate the Linked Service with. Changing this forces a new resource.
        :param pulumi.Input[str] description: The description for the Data Factory Linked Service MySQL.
        :param pulumi.Input[str] integration_runtime_name: The integration runtime reference to associate with the Data Factory Linked Service MySQL.
        :param pulumi.Input[str] name: Specifies the name of the Data Factory Linked Service MySQL. Changing this forces a new resource to be created. Must be globally unique. See the [Microsoft documentation](https://docs.microsoft.com/en-us/azure/data-factory/naming-rules) for all restrictions.
        :param pulumi.Input[dict] parameters: A map of parameters to associate with the Data Factory Linked Service MySQL.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Data Factory Linked Service MySQL. Changing this forces a new resource
        :param pulumi.Input[str] service_principal_id: The service principal id in which to authenticate against the Azure Data Lake Storage Gen2 account.
        :param pulumi.Input[str] service_principal_key: The service principal key in which to authenticate against the Azure Data Lake Storage Gen2 account.
        :param pulumi.Input[str] tenant: The tenant id or name in which to authenticate against the Azure Data Lake Storage Gen2 account.
        :param pulumi.Input[str] url: The endpoint for the Azure Data Lake Storage Gen2 service.
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

            __props__['additional_properties'] = additional_properties
            __props__['annotations'] = annotations
            if data_factory_name is None:
                raise TypeError("Missing required property 'data_factory_name'")
            __props__['data_factory_name'] = data_factory_name
            __props__['description'] = description
            __props__['integration_runtime_name'] = integration_runtime_name
            __props__['name'] = name
            __props__['parameters'] = parameters
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if service_principal_id is None:
                raise TypeError("Missing required property 'service_principal_id'")
            __props__['service_principal_id'] = service_principal_id
            if service_principal_key is None:
                raise TypeError("Missing required property 'service_principal_key'")
            __props__['service_principal_key'] = service_principal_key
            if tenant is None:
                raise TypeError("Missing required property 'tenant'")
            __props__['tenant'] = tenant
            if url is None:
                raise TypeError("Missing required property 'url'")
            __props__['url'] = url
        super(LinkedServiceDataLakeStorageGen2, __self__).__init__(
            'azure:datafactory/linkedServiceDataLakeStorageGen2:LinkedServiceDataLakeStorageGen2',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, additional_properties=None, annotations=None, data_factory_name=None, description=None, integration_runtime_name=None, name=None, parameters=None, resource_group_name=None, service_principal_id=None, service_principal_key=None, tenant=None, url=None):
        """
        Get an existing LinkedServiceDataLakeStorageGen2 resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] additional_properties: A map of additional properties to associate with the Data Factory Linked Service MySQL.
        :param pulumi.Input[list] annotations: List of tags that can be used for describing the Data Factory Linked Service MySQL.
        :param pulumi.Input[str] data_factory_name: The Data Factory name in which to associate the Linked Service with. Changing this forces a new resource.
        :param pulumi.Input[str] description: The description for the Data Factory Linked Service MySQL.
        :param pulumi.Input[str] integration_runtime_name: The integration runtime reference to associate with the Data Factory Linked Service MySQL.
        :param pulumi.Input[str] name: Specifies the name of the Data Factory Linked Service MySQL. Changing this forces a new resource to be created. Must be globally unique. See the [Microsoft documentation](https://docs.microsoft.com/en-us/azure/data-factory/naming-rules) for all restrictions.
        :param pulumi.Input[dict] parameters: A map of parameters to associate with the Data Factory Linked Service MySQL.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Data Factory Linked Service MySQL. Changing this forces a new resource
        :param pulumi.Input[str] service_principal_id: The service principal id in which to authenticate against the Azure Data Lake Storage Gen2 account.
        :param pulumi.Input[str] service_principal_key: The service principal key in which to authenticate against the Azure Data Lake Storage Gen2 account.
        :param pulumi.Input[str] tenant: The tenant id or name in which to authenticate against the Azure Data Lake Storage Gen2 account.
        :param pulumi.Input[str] url: The endpoint for the Azure Data Lake Storage Gen2 service.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["additional_properties"] = additional_properties
        __props__["annotations"] = annotations
        __props__["data_factory_name"] = data_factory_name
        __props__["description"] = description
        __props__["integration_runtime_name"] = integration_runtime_name
        __props__["name"] = name
        __props__["parameters"] = parameters
        __props__["resource_group_name"] = resource_group_name
        __props__["service_principal_id"] = service_principal_id
        __props__["service_principal_key"] = service_principal_key
        __props__["tenant"] = tenant
        __props__["url"] = url
        return LinkedServiceDataLakeStorageGen2(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

