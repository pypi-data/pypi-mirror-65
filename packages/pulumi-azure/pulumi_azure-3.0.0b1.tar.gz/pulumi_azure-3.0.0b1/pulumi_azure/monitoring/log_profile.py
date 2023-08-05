# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class LogProfile(pulumi.CustomResource):
    categories: pulumi.Output[list]
    """
    List of categories of the logs.
    """
    locations: pulumi.Output[list]
    """
    List of regions for which Activity Log events are stored or streamed.
    """
    name: pulumi.Output[str]
    """
    The name of the Log Profile. Changing this forces a
    new resource to be created.
    """
    retention_policy: pulumi.Output[dict]
    """
    A `retention_policy` block as documented below. A retention policy for how long Activity Logs are retained in the storage account.

      * `days` (`float`) - The number of days for the retention policy. Defaults to 0.
      * `enabled` (`bool`) - A boolean value to indicate whether the retention policy is enabled.
    """
    servicebus_rule_id: pulumi.Output[str]
    """
    The service bus (or event hub) rule ID of the service bus (or event hub) namespace in which the Activity Log is streamed to. At least one of `storage_account_id` or `servicebus_rule_id` must be set.
    """
    storage_account_id: pulumi.Output[str]
    """
    The resource ID of the storage account in which the Activity Log is stored. At least one of `storage_account_id` or `servicebus_rule_id` must be set.
    """
    def __init__(__self__, resource_name, opts=None, categories=None, locations=None, name=None, retention_policy=None, servicebus_rule_id=None, storage_account_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a [Log Profile](https://docs.microsoft.com/en-us/azure/monitoring-and-diagnostics/monitoring-overview-activity-logs#export-the-activity-log-with-a-log-profile). A Log Profile configures how Activity Logs are exported.

        > **NOTE:** It's only possible to configure one Log Profile per Subscription. If you are trying to create more than one Log Profile, an error with `StatusCode=409` will occur.



        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/monitor_log_profile.html.markdown.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] categories: List of categories of the logs.
        :param pulumi.Input[list] locations: List of regions for which Activity Log events are stored or streamed.
        :param pulumi.Input[str] name: The name of the Log Profile. Changing this forces a
               new resource to be created.
        :param pulumi.Input[dict] retention_policy: A `retention_policy` block as documented below. A retention policy for how long Activity Logs are retained in the storage account.
        :param pulumi.Input[str] servicebus_rule_id: The service bus (or event hub) rule ID of the service bus (or event hub) namespace in which the Activity Log is streamed to. At least one of `storage_account_id` or `servicebus_rule_id` must be set.
        :param pulumi.Input[str] storage_account_id: The resource ID of the storage account in which the Activity Log is stored. At least one of `storage_account_id` or `servicebus_rule_id` must be set.

        The **retention_policy** object supports the following:

          * `days` (`pulumi.Input[float]`) - The number of days for the retention policy. Defaults to 0.
          * `enabled` (`pulumi.Input[bool]`) - A boolean value to indicate whether the retention policy is enabled.
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

            if categories is None:
                raise TypeError("Missing required property 'categories'")
            __props__['categories'] = categories
            if locations is None:
                raise TypeError("Missing required property 'locations'")
            __props__['locations'] = locations
            __props__['name'] = name
            if retention_policy is None:
                raise TypeError("Missing required property 'retention_policy'")
            __props__['retention_policy'] = retention_policy
            __props__['servicebus_rule_id'] = servicebus_rule_id
            __props__['storage_account_id'] = storage_account_id
        super(LogProfile, __self__).__init__(
            'azure:monitoring/logProfile:LogProfile',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, categories=None, locations=None, name=None, retention_policy=None, servicebus_rule_id=None, storage_account_id=None):
        """
        Get an existing LogProfile resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] categories: List of categories of the logs.
        :param pulumi.Input[list] locations: List of regions for which Activity Log events are stored or streamed.
        :param pulumi.Input[str] name: The name of the Log Profile. Changing this forces a
               new resource to be created.
        :param pulumi.Input[dict] retention_policy: A `retention_policy` block as documented below. A retention policy for how long Activity Logs are retained in the storage account.
        :param pulumi.Input[str] servicebus_rule_id: The service bus (or event hub) rule ID of the service bus (or event hub) namespace in which the Activity Log is streamed to. At least one of `storage_account_id` or `servicebus_rule_id` must be set.
        :param pulumi.Input[str] storage_account_id: The resource ID of the storage account in which the Activity Log is stored. At least one of `storage_account_id` or `servicebus_rule_id` must be set.

        The **retention_policy** object supports the following:

          * `days` (`pulumi.Input[float]`) - The number of days for the retention policy. Defaults to 0.
          * `enabled` (`pulumi.Input[bool]`) - A boolean value to indicate whether the retention policy is enabled.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["categories"] = categories
        __props__["locations"] = locations
        __props__["name"] = name
        __props__["retention_policy"] = retention_policy
        __props__["servicebus_rule_id"] = servicebus_rule_id
        __props__["storage_account_id"] = storage_account_id
        return LogProfile(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

