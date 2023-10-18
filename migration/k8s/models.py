from dataclasses import dataclass

from lightkube.core.dataclasses_dict import DataclassDictMixIn
from lightkube.models import meta_v1


@dataclass
class OpenSearch(DataclassDictMixIn):
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    spec: 'OpenSearchSpec' = None
    status: 'OpenSearchStatus' = None


@dataclass
class OpenSearchSpec(DataclassDictMixIn):
    plan: 'str'
    project: 'str'
    cloudName: 'str' = None
    projectVpcId: 'str' = None
    tags: 'dict' = None
    terminationProtection: 'bool' = None


@dataclass
class OpenSearchStatus(DataclassDictMixIn):
    conditions: 'List[meta_v1.Condition]' = None
    state: 'str' = None
