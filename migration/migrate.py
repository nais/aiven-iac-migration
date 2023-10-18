import textwrap

from lightkube import KubeConfig, Client, codecs
from lightkube.resources.core_v1 import Service
from lightkube.generic_resource import create_namespaced_resource

from .aiven import Aiven
from .errors import MigrateError


def _create_service_resource(project, service):
    return codecs.load_all_yaml(textwrap.dedent(f"""\
    apiVersion: aiven.io/v1alpha1
    kind: OpenSearch
    metadata:
        name: {service.service_name}
        namespace: {service.tags["team"]}
        annotations:
            nais.io/created_by: aiven-iac-migration
        labels:
            team: {service.tags["team"]}
    spec:
        plan: {service.plan}
        project: {project}
        cloudName: {service.cloud_name}
        projectVpcId: {service.project_vpc_id}
        tags:
            team: {service.tags["team"]}
            environment: {service.tags["environment"]}
            tenant: {service.tags["tenant"]}
        terminationProtection: {service.termination_protection}
    """), context={"service": service})


def _create_service_integration_resource(service):
    pass


def _migrate_service(project, service, client):
    resource = _create_service_resource(project, service)
    print(resource)
    integration = _create_service_integration_resource(service)


def _create_k8s_client(options) -> Client:
    k8s_context = f"{options.tenant}-{options.env}"
    if options.tenant == "nav":
        k8s_context += "-gcp"
    try:
        config = KubeConfig.from_env()
        client = Client(config.get(context_name=k8s_context))
        client.get(Service, "kubernetes", namespace="default")
        create_namespaced_resource("aiven.io", "v1alpha1", "OpenSearch", "opensearches")
    except Exception as e:
        raise MigrateError(f"Unable to connect to kubernetes cluster {k8s_context}") from e
    return client


def migrate(options):
    aiven_project = f"{options.tenant}-{options.env}"
    client = _create_k8s_client(options)
    aiven = Aiven(aiven_project)
    for service in aiven.get_services():
        if service.service_type == options.service_type:
            _migrate_service(aiven_project, service, client)
