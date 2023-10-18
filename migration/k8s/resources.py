
from lightkube.core import resource as res

from . import models


class OpenSearch(res.NamespacedResourceG, models.OpenSearch):
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('aiven.io', 'v1alpha1', 'OpenSearch'),
        plural='opensearches',
        verbs=['delete', 'deletecollection', 'get', 'global_list', 'global_watch', 'list', 'patch', 'post', 'put', 'watch'],
    )
