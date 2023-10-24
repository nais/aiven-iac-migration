from typing import ClassVar

from lightkube.core import resource as res

from . import models


########################################################################################################################
# OpenSearch
########################################################################################################################

class OpenSearchStatus(res.NamespacedSubResource, models.OpenSearch):
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('aiven.io', 'v1alpha1', 'OpenSearch'),
        parent=res.ResourceDef('aiven.io', 'v1alpha1', 'OpenSearch'),
        plural='opensearches',
        verbs=['get', 'patch', 'put'],
        action='status',
    )


class OpenSearch(res.NamespacedResourceG, models.OpenSearch):
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('aiven.io', 'v1alpha1', 'OpenSearch'),
        plural='opensearches',
        verbs=['delete', 'deletecollection', 'get', 'global_list', 'global_watch', 'list', 'patch', 'post', 'put',
               'watch'],
    )

    Status: ClassVar = OpenSearchStatus


########################################################################################################################
# ServiceIntegration
########################################################################################################################

class ServiceIntegrationStatus(res.NamespacedSubResource, models.ServiceIntegration):
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('aiven.io', 'v1alpha1', 'ServiceIntegration'),
        parent=res.ResourceDef('aiven.io', 'v1alpha1', 'ServiceIntegration'),
        plural='serviceintegrations',
        verbs=['get', 'patch', 'put'],
        action='status',
    )


class ServiceIntegration(res.NamespacedResourceG, models.ServiceIntegration):
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('aiven.io', 'v1alpha1', 'ServiceIntegration'),
        plural='serviceintegrations',
        verbs=['delete', 'deletecollection', 'get', 'global_list', 'global_watch', 'list', 'patch', 'post', 'put',
               'watch'],
    )

    Status: ClassVar = ServiceIntegrationStatus
