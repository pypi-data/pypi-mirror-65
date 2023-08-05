# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class EventhubDataConnection(pulumi.CustomResource):
    cluster_name: pulumi.Output[str]
    """
    Specifies the name of the Kusto Cluster this data connection will be added to. Changing this forces a new resource to be created.
    """
    consumer_group: pulumi.Output[str]
    """
    Specifies the EventHub consumer group this data connection will use for ingestion. Changing this forces a new resource to be created.
    """
    data_format: pulumi.Output[str]
    """
    Specifies the data format of the EventHub messages. Allowed values: `AVRO`, `CSV`, `JSON`, `MULTIJSON`, `PSV`, `RAW`, `SCSV`, `SINGLEJSON`, `SOHSV`, `TSV` and `TXT`
    """
    database_name: pulumi.Output[str]
    """
    Specifies the name of the Kusto Database this data connection will be added to. Changing this forces a new resource to be created.
    """
    eventhub_id: pulumi.Output[str]
    """
    Specifies the resource id of the EventHub this data connection will use for ingestion. Changing this forces a new resource to be created.
    """
    location: pulumi.Output[str]
    """
    The location where the Kusto Database should be created. Changing this forces a new resource to be created.
    """
    mapping_rule_name: pulumi.Output[str]
    """
    Specifies the mapping rule used for the message ingestion. Mapping rule must exist before resource is created.
    """
    name: pulumi.Output[str]
    """
    The name of the Kusto EventHub Data Connection to create. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    Specifies the Resource Group where the Kusto Database should exist. Changing this forces a new resource to be created.
    """
    table_name: pulumi.Output[str]
    """
    Specifies the target table name used for the message ingestion. Table must exist before resource is created.
    """
    def __init__(__self__, resource_name, opts=None, cluster_name=None, consumer_group=None, data_format=None, database_name=None, eventhub_id=None, location=None, mapping_rule_name=None, name=None, resource_group_name=None, table_name=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a Kusto (also known as Azure Data Explorer) EventHub Data Connection



        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/kusto_eventhub_data_connection.html.markdown.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_name: Specifies the name of the Kusto Cluster this data connection will be added to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] consumer_group: Specifies the EventHub consumer group this data connection will use for ingestion. Changing this forces a new resource to be created.
        :param pulumi.Input[str] data_format: Specifies the data format of the EventHub messages. Allowed values: `AVRO`, `CSV`, `JSON`, `MULTIJSON`, `PSV`, `RAW`, `SCSV`, `SINGLEJSON`, `SOHSV`, `TSV` and `TXT`
        :param pulumi.Input[str] database_name: Specifies the name of the Kusto Database this data connection will be added to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] eventhub_id: Specifies the resource id of the EventHub this data connection will use for ingestion. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: The location where the Kusto Database should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] mapping_rule_name: Specifies the mapping rule used for the message ingestion. Mapping rule must exist before resource is created.
        :param pulumi.Input[str] name: The name of the Kusto EventHub Data Connection to create. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: Specifies the Resource Group where the Kusto Database should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] table_name: Specifies the target table name used for the message ingestion. Table must exist before resource is created.
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

            if cluster_name is None:
                raise TypeError("Missing required property 'cluster_name'")
            __props__['cluster_name'] = cluster_name
            if consumer_group is None:
                raise TypeError("Missing required property 'consumer_group'")
            __props__['consumer_group'] = consumer_group
            __props__['data_format'] = data_format
            if database_name is None:
                raise TypeError("Missing required property 'database_name'")
            __props__['database_name'] = database_name
            if eventhub_id is None:
                raise TypeError("Missing required property 'eventhub_id'")
            __props__['eventhub_id'] = eventhub_id
            __props__['location'] = location
            __props__['mapping_rule_name'] = mapping_rule_name
            __props__['name'] = name
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['table_name'] = table_name
        super(EventhubDataConnection, __self__).__init__(
            'azure:kusto/eventhubDataConnection:EventhubDataConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, cluster_name=None, consumer_group=None, data_format=None, database_name=None, eventhub_id=None, location=None, mapping_rule_name=None, name=None, resource_group_name=None, table_name=None):
        """
        Get an existing EventhubDataConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_name: Specifies the name of the Kusto Cluster this data connection will be added to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] consumer_group: Specifies the EventHub consumer group this data connection will use for ingestion. Changing this forces a new resource to be created.
        :param pulumi.Input[str] data_format: Specifies the data format of the EventHub messages. Allowed values: `AVRO`, `CSV`, `JSON`, `MULTIJSON`, `PSV`, `RAW`, `SCSV`, `SINGLEJSON`, `SOHSV`, `TSV` and `TXT`
        :param pulumi.Input[str] database_name: Specifies the name of the Kusto Database this data connection will be added to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] eventhub_id: Specifies the resource id of the EventHub this data connection will use for ingestion. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: The location where the Kusto Database should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] mapping_rule_name: Specifies the mapping rule used for the message ingestion. Mapping rule must exist before resource is created.
        :param pulumi.Input[str] name: The name of the Kusto EventHub Data Connection to create. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: Specifies the Resource Group where the Kusto Database should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] table_name: Specifies the target table name used for the message ingestion. Table must exist before resource is created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["cluster_name"] = cluster_name
        __props__["consumer_group"] = consumer_group
        __props__["data_format"] = data_format
        __props__["database_name"] = database_name
        __props__["eventhub_id"] = eventhub_id
        __props__["location"] = location
        __props__["mapping_rule_name"] = mapping_rule_name
        __props__["name"] = name
        __props__["resource_group_name"] = resource_group_name
        __props__["table_name"] = table_name
        return EventhubDataConnection(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

