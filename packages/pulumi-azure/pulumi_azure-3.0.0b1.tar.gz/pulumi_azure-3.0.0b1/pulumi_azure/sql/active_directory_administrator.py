# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class ActiveDirectoryAdministrator(pulumi.CustomResource):
    login: pulumi.Output[str]
    """
    The login name of the principal to set as the server administrator
    """
    object_id: pulumi.Output[str]
    """
    The ID of the principal to set as the server administrator
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group for the SQL server. Changing this forces a new resource to be created.
    """
    server_name: pulumi.Output[str]
    """
    The name of the SQL Server on which to set the administrator. Changing this forces a new resource to be created.
    """
    tenant_id: pulumi.Output[str]
    """
    The Azure Tenant ID
    """
    def __init__(__self__, resource_name, opts=None, login=None, object_id=None, resource_group_name=None, server_name=None, tenant_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Allows you to set a user or group as the AD administrator for an Azure SQL server



        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/sql_active_directory_administrator.markdown.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] login: The login name of the principal to set as the server administrator
        :param pulumi.Input[str] object_id: The ID of the principal to set as the server administrator
        :param pulumi.Input[str] resource_group_name: The name of the resource group for the SQL server. Changing this forces a new resource to be created.
        :param pulumi.Input[str] server_name: The name of the SQL Server on which to set the administrator. Changing this forces a new resource to be created.
        :param pulumi.Input[str] tenant_id: The Azure Tenant ID
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

            if login is None:
                raise TypeError("Missing required property 'login'")
            __props__['login'] = login
            if object_id is None:
                raise TypeError("Missing required property 'object_id'")
            __props__['object_id'] = object_id
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if server_name is None:
                raise TypeError("Missing required property 'server_name'")
            __props__['server_name'] = server_name
            if tenant_id is None:
                raise TypeError("Missing required property 'tenant_id'")
            __props__['tenant_id'] = tenant_id
        super(ActiveDirectoryAdministrator, __self__).__init__(
            'azure:sql/activeDirectoryAdministrator:ActiveDirectoryAdministrator',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, login=None, object_id=None, resource_group_name=None, server_name=None, tenant_id=None):
        """
        Get an existing ActiveDirectoryAdministrator resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] login: The login name of the principal to set as the server administrator
        :param pulumi.Input[str] object_id: The ID of the principal to set as the server administrator
        :param pulumi.Input[str] resource_group_name: The name of the resource group for the SQL server. Changing this forces a new resource to be created.
        :param pulumi.Input[str] server_name: The name of the SQL Server on which to set the administrator. Changing this forces a new resource to be created.
        :param pulumi.Input[str] tenant_id: The Azure Tenant ID
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["login"] = login
        __props__["object_id"] = object_id
        __props__["resource_group_name"] = resource_group_name
        __props__["server_name"] = server_name
        __props__["tenant_id"] = tenant_id
        return ActiveDirectoryAdministrator(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

