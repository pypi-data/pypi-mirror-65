# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class TxtRecord(pulumi.CustomResource):
    fqdn: pulumi.Output[str]
    """
    The FQDN of the DNS TXT Record.
    """
    name: pulumi.Output[str]
    """
    The name of the DNS TXT Record.
    """
    records: pulumi.Output[list]
    """
    A list of values that make up the txt record. Each `record` block supports fields documented below.

      * `value` (`str`) - The value of the record. Max length: 1024 characters
    """
    resource_group_name: pulumi.Output[str]
    """
    Specifies the resource group where the resource exists. Changing this forces a new resource to be created.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    ttl: pulumi.Output[float]
    """
    The Time To Live (TTL) of the DNS record in seconds.
    """
    zone_name: pulumi.Output[str]
    """
    Specifies the DNS Zone where the DNS Zone (parent resource) exists. Changing this forces a new resource to be created.
    """
    def __init__(__self__, resource_name, opts=None, name=None, records=None, resource_group_name=None, tags=None, ttl=None, zone_name=None, __props__=None, __name__=None, __opts__=None):
        """
        Enables you to manage DNS TXT Records within Azure DNS.



        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/dns_txt_record.html.markdown.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the DNS TXT Record.
        :param pulumi.Input[list] records: A list of values that make up the txt record. Each `record` block supports fields documented below.
        :param pulumi.Input[str] resource_group_name: Specifies the resource group where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[float] ttl: The Time To Live (TTL) of the DNS record in seconds.
        :param pulumi.Input[str] zone_name: Specifies the DNS Zone where the DNS Zone (parent resource) exists. Changing this forces a new resource to be created.

        The **records** object supports the following:

          * `value` (`pulumi.Input[str]`) - The value of the record. Max length: 1024 characters
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

            __props__['name'] = name
            if records is None:
                raise TypeError("Missing required property 'records'")
            __props__['records'] = records
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tags'] = tags
            if ttl is None:
                raise TypeError("Missing required property 'ttl'")
            __props__['ttl'] = ttl
            if zone_name is None:
                raise TypeError("Missing required property 'zone_name'")
            __props__['zone_name'] = zone_name
            __props__['fqdn'] = None
        super(TxtRecord, __self__).__init__(
            'azure:dns/txtRecord:TxtRecord',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, fqdn=None, name=None, records=None, resource_group_name=None, tags=None, ttl=None, zone_name=None):
        """
        Get an existing TxtRecord resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] fqdn: The FQDN of the DNS TXT Record.
        :param pulumi.Input[str] name: The name of the DNS TXT Record.
        :param pulumi.Input[list] records: A list of values that make up the txt record. Each `record` block supports fields documented below.
        :param pulumi.Input[str] resource_group_name: Specifies the resource group where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[float] ttl: The Time To Live (TTL) of the DNS record in seconds.
        :param pulumi.Input[str] zone_name: Specifies the DNS Zone where the DNS Zone (parent resource) exists. Changing this forces a new resource to be created.

        The **records** object supports the following:

          * `value` (`pulumi.Input[str]`) - The value of the record. Max length: 1024 characters
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["fqdn"] = fqdn
        __props__["name"] = name
        __props__["records"] = records
        __props__["resource_group_name"] = resource_group_name
        __props__["tags"] = tags
        __props__["ttl"] = ttl
        __props__["zone_name"] = zone_name
        return TxtRecord(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

