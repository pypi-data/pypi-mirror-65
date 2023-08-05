# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class DpsSharedAccessPolicy(pulumi.CustomResource):
    enrollment_read: pulumi.Output[bool]
    """
    Adds `EnrollmentRead` permission to this Shared Access Account. It allows read access to enrollment data.
    """
    enrollment_write: pulumi.Output[bool]
    """
    Adds `EnrollmentWrite` permission to this Shared Access Account. It allows write access to enrollment data.
    """
    iothub_dps_name: pulumi.Output[str]
    """
    The name of the IoT Hub Device Provisioning service to which this Shared Access Policy belongs. Changing this forces a new resource to be created.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the IotHub Shared Access Policy resource. Changing this forces a new resource to be created.
    """
    primary_connection_string: pulumi.Output[str]
    """
    The primary connection string of the Shared Access Policy.
    """
    primary_key: pulumi.Output[str]
    """
    The primary key used to create the authentication token.
    """
    registration_read: pulumi.Output[bool]
    """
    Adds `RegistrationStatusRead` permission to this Shared Access Account. It allows read access to device registrations.
    """
    registration_write: pulumi.Output[bool]
    """
    Adds `RegistrationStatusWrite` permission to this Shared Access Account. It allows write access to device registrations.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group under which the IotHub Shared Access Policy resource has to be created. Changing this forces a new resource to be created.
    """
    secondary_connection_string: pulumi.Output[str]
    """
    The secondary connection string of the Shared Access Policy.
    """
    secondary_key: pulumi.Output[str]
    """
    The secondary key used to create the authentication token.
    """
    service_config: pulumi.Output[bool]
    """
    Adds `ServiceConfig` permission to this Shared Access Account. It allows configuration of the Device Provisioning Service.
    """
    def __init__(__self__, resource_name, opts=None, enrollment_read=None, enrollment_write=None, iothub_dps_name=None, name=None, registration_read=None, registration_write=None, resource_group_name=None, service_config=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an IotHub Device Provisioning Service Shared Access Policy



        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/iothub_dps_shared_access_policy.html.markdown.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enrollment_read: Adds `EnrollmentRead` permission to this Shared Access Account. It allows read access to enrollment data.
        :param pulumi.Input[bool] enrollment_write: Adds `EnrollmentWrite` permission to this Shared Access Account. It allows write access to enrollment data.
        :param pulumi.Input[str] iothub_dps_name: The name of the IoT Hub Device Provisioning service to which this Shared Access Policy belongs. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the IotHub Shared Access Policy resource. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] registration_read: Adds `RegistrationStatusRead` permission to this Shared Access Account. It allows read access to device registrations.
        :param pulumi.Input[bool] registration_write: Adds `RegistrationStatusWrite` permission to this Shared Access Account. It allows write access to device registrations.
        :param pulumi.Input[str] resource_group_name: The name of the resource group under which the IotHub Shared Access Policy resource has to be created. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] service_config: Adds `ServiceConfig` permission to this Shared Access Account. It allows configuration of the Device Provisioning Service.
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

            __props__['enrollment_read'] = enrollment_read
            __props__['enrollment_write'] = enrollment_write
            if iothub_dps_name is None:
                raise TypeError("Missing required property 'iothub_dps_name'")
            __props__['iothub_dps_name'] = iothub_dps_name
            __props__['name'] = name
            __props__['registration_read'] = registration_read
            __props__['registration_write'] = registration_write
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['service_config'] = service_config
            __props__['primary_connection_string'] = None
            __props__['primary_key'] = None
            __props__['secondary_connection_string'] = None
            __props__['secondary_key'] = None
        super(DpsSharedAccessPolicy, __self__).__init__(
            'azure:iot/dpsSharedAccessPolicy:DpsSharedAccessPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, enrollment_read=None, enrollment_write=None, iothub_dps_name=None, name=None, primary_connection_string=None, primary_key=None, registration_read=None, registration_write=None, resource_group_name=None, secondary_connection_string=None, secondary_key=None, service_config=None):
        """
        Get an existing DpsSharedAccessPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enrollment_read: Adds `EnrollmentRead` permission to this Shared Access Account. It allows read access to enrollment data.
        :param pulumi.Input[bool] enrollment_write: Adds `EnrollmentWrite` permission to this Shared Access Account. It allows write access to enrollment data.
        :param pulumi.Input[str] iothub_dps_name: The name of the IoT Hub Device Provisioning service to which this Shared Access Policy belongs. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the IotHub Shared Access Policy resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] primary_connection_string: The primary connection string of the Shared Access Policy.
        :param pulumi.Input[str] primary_key: The primary key used to create the authentication token.
        :param pulumi.Input[bool] registration_read: Adds `RegistrationStatusRead` permission to this Shared Access Account. It allows read access to device registrations.
        :param pulumi.Input[bool] registration_write: Adds `RegistrationStatusWrite` permission to this Shared Access Account. It allows write access to device registrations.
        :param pulumi.Input[str] resource_group_name: The name of the resource group under which the IotHub Shared Access Policy resource has to be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] secondary_connection_string: The secondary connection string of the Shared Access Policy.
        :param pulumi.Input[str] secondary_key: The secondary key used to create the authentication token.
        :param pulumi.Input[bool] service_config: Adds `ServiceConfig` permission to this Shared Access Account. It allows configuration of the Device Provisioning Service.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["enrollment_read"] = enrollment_read
        __props__["enrollment_write"] = enrollment_write
        __props__["iothub_dps_name"] = iothub_dps_name
        __props__["name"] = name
        __props__["primary_connection_string"] = primary_connection_string
        __props__["primary_key"] = primary_key
        __props__["registration_read"] = registration_read
        __props__["registration_write"] = registration_write
        __props__["resource_group_name"] = resource_group_name
        __props__["secondary_connection_string"] = secondary_connection_string
        __props__["secondary_key"] = secondary_key
        __props__["service_config"] = service_config
        return DpsSharedAccessPolicy(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

