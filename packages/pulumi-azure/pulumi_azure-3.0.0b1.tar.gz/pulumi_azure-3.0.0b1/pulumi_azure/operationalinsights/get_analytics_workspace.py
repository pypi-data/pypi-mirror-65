# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetAnalyticsWorkspaceResult:
    """
    A collection of values returned by getAnalyticsWorkspace.
    """
    def __init__(__self__, id=None, location=None, name=None, portal_url=None, primary_shared_key=None, resource_group_name=None, retention_in_days=None, secondary_shared_key=None, sku=None, tags=None, workspace_id=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        __self__.location = location
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if portal_url and not isinstance(portal_url, str):
            raise TypeError("Expected argument 'portal_url' to be a str")
        __self__.portal_url = portal_url
        """
        The Portal URL for the Log Analytics Workspace.
        """
        if primary_shared_key and not isinstance(primary_shared_key, str):
            raise TypeError("Expected argument 'primary_shared_key' to be a str")
        __self__.primary_shared_key = primary_shared_key
        """
        The Primary shared key for the Log Analytics Workspace.
        """
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if retention_in_days and not isinstance(retention_in_days, float):
            raise TypeError("Expected argument 'retention_in_days' to be a float")
        __self__.retention_in_days = retention_in_days
        """
        The workspace data retention in days.
        """
        if secondary_shared_key and not isinstance(secondary_shared_key, str):
            raise TypeError("Expected argument 'secondary_shared_key' to be a str")
        __self__.secondary_shared_key = secondary_shared_key
        """
        The Secondary shared key for the Log Analytics Workspace.
        """
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        __self__.sku = sku
        """
        The Sku of the Log Analytics Workspace.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A mapping of tags assigned to the resource.
        """
        if workspace_id and not isinstance(workspace_id, str):
            raise TypeError("Expected argument 'workspace_id' to be a str")
        __self__.workspace_id = workspace_id
        """
        The Workspace (or Customer) ID for the Log Analytics Workspace.
        """
class AwaitableGetAnalyticsWorkspaceResult(GetAnalyticsWorkspaceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAnalyticsWorkspaceResult(
            id=self.id,
            location=self.location,
            name=self.name,
            portal_url=self.portal_url,
            primary_shared_key=self.primary_shared_key,
            resource_group_name=self.resource_group_name,
            retention_in_days=self.retention_in_days,
            secondary_shared_key=self.secondary_shared_key,
            sku=self.sku,
            tags=self.tags,
            workspace_id=self.workspace_id)

def get_analytics_workspace(name=None,resource_group_name=None,opts=None):
    """
    Use this data source to access information about an existing Log Analytics (formally Operational Insights) Workspace.



    > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/d/log_analytics_workspace.html.markdown.


    :param str name: Specifies the name of the Log Analytics Workspace.
    :param str resource_group_name: The name of the resource group in which the Log Analytics workspace is located in.
    """
    __args__ = dict()


    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:operationalinsights/getAnalyticsWorkspace:getAnalyticsWorkspace', __args__, opts=opts).value

    return AwaitableGetAnalyticsWorkspaceResult(
        id=__ret__.get('id'),
        location=__ret__.get('location'),
        name=__ret__.get('name'),
        portal_url=__ret__.get('portalUrl'),
        primary_shared_key=__ret__.get('primarySharedKey'),
        resource_group_name=__ret__.get('resourceGroupName'),
        retention_in_days=__ret__.get('retentionInDays'),
        secondary_shared_key=__ret__.get('secondarySharedKey'),
        sku=__ret__.get('sku'),
        tags=__ret__.get('tags'),
        workspace_id=__ret__.get('workspaceId'))
