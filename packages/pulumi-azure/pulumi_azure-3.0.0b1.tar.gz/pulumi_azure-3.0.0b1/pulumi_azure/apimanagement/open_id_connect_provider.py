# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class OpenIdConnectProvider(pulumi.CustomResource):
    api_management_name: pulumi.Output[str]
    """
    The name of the API Management Service in which this OpenID Connect Provider should be created. Changing this forces a new resource to be created.
    """
    client_id: pulumi.Output[str]
    """
    The Client ID used for the Client Application.
    """
    client_secret: pulumi.Output[str]
    """
    The Client Secret used for the Client Application.
    """
    description: pulumi.Output[str]
    """
    A description of this OpenID Connect Provider.
    """
    display_name: pulumi.Output[str]
    """
    A user-friendly name for this OpenID Connect Provider.
    """
    metadata_endpoint: pulumi.Output[str]
    """
    The URI of the Metadata endpoint.
    """
    name: pulumi.Output[str]
    """
    the Name of the OpenID Connect Provider which should be created within the API Management Service. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the Resource Group where the API Management Service exists. Changing this forces a new resource to be created.
    """
    def __init__(__self__, resource_name, opts=None, api_management_name=None, client_id=None, client_secret=None, description=None, display_name=None, metadata_endpoint=None, name=None, resource_group_name=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an OpenID Connect Provider within a API Management Service.



        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/api_management_openid_connect_provider.html.markdown.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The name of the API Management Service in which this OpenID Connect Provider should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] client_id: The Client ID used for the Client Application.
        :param pulumi.Input[str] client_secret: The Client Secret used for the Client Application.
        :param pulumi.Input[str] description: A description of this OpenID Connect Provider.
        :param pulumi.Input[str] display_name: A user-friendly name for this OpenID Connect Provider.
        :param pulumi.Input[str] metadata_endpoint: The URI of the Metadata endpoint.
        :param pulumi.Input[str] name: the Name of the OpenID Connect Provider which should be created within the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the API Management Service exists. Changing this forces a new resource to be created.
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

            if api_management_name is None:
                raise TypeError("Missing required property 'api_management_name'")
            __props__['api_management_name'] = api_management_name
            if client_id is None:
                raise TypeError("Missing required property 'client_id'")
            __props__['client_id'] = client_id
            if client_secret is None:
                raise TypeError("Missing required property 'client_secret'")
            __props__['client_secret'] = client_secret
            __props__['description'] = description
            if display_name is None:
                raise TypeError("Missing required property 'display_name'")
            __props__['display_name'] = display_name
            if metadata_endpoint is None:
                raise TypeError("Missing required property 'metadata_endpoint'")
            __props__['metadata_endpoint'] = metadata_endpoint
            __props__['name'] = name
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
        super(OpenIdConnectProvider, __self__).__init__(
            'azure:apimanagement/openIdConnectProvider:OpenIdConnectProvider',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, api_management_name=None, client_id=None, client_secret=None, description=None, display_name=None, metadata_endpoint=None, name=None, resource_group_name=None):
        """
        Get an existing OpenIdConnectProvider resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The name of the API Management Service in which this OpenID Connect Provider should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] client_id: The Client ID used for the Client Application.
        :param pulumi.Input[str] client_secret: The Client Secret used for the Client Application.
        :param pulumi.Input[str] description: A description of this OpenID Connect Provider.
        :param pulumi.Input[str] display_name: A user-friendly name for this OpenID Connect Provider.
        :param pulumi.Input[str] metadata_endpoint: The URI of the Metadata endpoint.
        :param pulumi.Input[str] name: the Name of the OpenID Connect Provider which should be created within the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the API Management Service exists. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["api_management_name"] = api_management_name
        __props__["client_id"] = client_id
        __props__["client_secret"] = client_secret
        __props__["description"] = description
        __props__["display_name"] = display_name
        __props__["metadata_endpoint"] = metadata_endpoint
        __props__["name"] = name
        __props__["resource_group_name"] = resource_group_name
        return OpenIdConnectProvider(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

