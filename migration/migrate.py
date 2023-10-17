from lightkube import KubeConfig, Client
from lightkube.resources.core_v1 import Service

from .aiven import Aiven
from .errors import MigrateError


def _create_service_resource(service):
    pass


def _create_service_integration_resource(service):
    pass


def _migrate_service(service, client):
    resource = _create_service_resource(service)
    integration = _create_service_integration_resource(service)


def _create_k8s_client(options) -> Client:
    k8s_context = f"nav-{options.env}-gcp"
    try:
        config = KubeConfig.from_env()
        client = Client(config.get(context_name=k8s_context))
        client.get(Service, "kubernetes", namespace="default")
    except Exception as e:
        raise MigrateError(f"Unable to connect to kubernetes cluster {k8s_context}") from e
    return client


def migrate(options):
    aiven_project = f"nav-{options.env}"
    client = _create_k8s_client(options)
    aiven = Aiven(aiven_project)
    for service in aiven.get_services():
        if service.service_type == options.service_type:
            _migrate_service(service, client)
