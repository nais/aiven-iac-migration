import textwrap

import yaml
from lightkube import KubeConfig, Client, codecs
from lightkube.generic_resource import create_namespaced_resource
from lightkube.resources.core_v1 import Service
from rich import print
from rich.progress import Progress

from .aiven import Aiven
from .errors import KubernetesError
from .k8s.resources import OpenSearch, ServiceIntegration


def _find_prometheus_integration(service):
    for integration in service.service_integrations:
        if integration.integration_type == "prometheus":
            return integration


def _create_resources(project, service):
    resources = []
    prometheus = _find_prometheus_integration(service)
    resources.append(OpenSearch.from_dict(yaml.safe_load(textwrap.dedent(f"""\
    ---
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
        disk_space: "{service.disk_space_mb // 1024}G"
        projectVpcId: {service.project_vpc_id}
        tags:
            team: {service.tags["team"]}
            environment: {service.tags["environment"]}
            tenant: {service.tags["tenant"]}
        terminationProtection: {service.termination_protection}
    """))))
    if prometheus:
        service_integration_data = yaml.safe_load(textwrap.dedent(f"""\
        ---
        apiVersion: aiven.io/v1alpha1
        kind: ServiceIntegration
        metadata:
            name: {service.service_name}-prometheus
            namespace: {service.tags["team"]}
            annotations:
                nais.io/created_by: aiven-iac-migration
            labels:
                team: {service.tags["team"]}
        spec:
            project: {project}
            integrationType: prometheus
            destinationEndpointId: {prometheus.dest_endpoint_id}
            sourceServiceName: {service.service_name}
        status:
            conditions: []
            id: {prometheus.service_integration_id}
        """))
        resources.append(ServiceIntegration.from_dict(service_integration_data))
        resources.append(ServiceIntegration.Status.from_dict(service_integration_data))
    return resources


def _migrate_service(project, service, client: Client, dry_run):
    resources = _create_resources(project, service)
    if not dry_run:
        for item in resources:
            print(f"\n[blue]Applying:[/blue] [yellow]{item.kind}[/yellow]/[green]{item.metadata.name}[/green] in namespace [red]{item.metadata.namespace}[/red] ...")
            client.apply(item, namespace=item.metadata.namespace)
    else:
        print("\n[blue]Would have applied the following items:[/blue]")
        print(codecs.dump_all_yaml(resources))


def _create_k8s_client(options) -> Client:
    k8s_context = f"{options.tenant}-{options.env}"
    if options.tenant == "nav":
        k8s_context += "-gcp"
    try:
        config = KubeConfig.from_env()
        client = Client(config.get(context_name=k8s_context), field_manager="aiven-iac-migration")
        client.get(Service, "kubernetes", namespace="default")
        create_namespaced_resource("aiven.io", "v1alpha1", "OpenSearch", "opensearches")
        create_namespaced_resource("aiven.io", "v1alpha1", "ServiceIntegration", "serviceintegrations")
    except Exception as e:
        raise KubernetesError(f"Unable to connect to kubernetes cluster {k8s_context}") from e
    return client


def migrate(options, console):
    aiven_project = f"{options.tenant}-{options.env}"
    client = _create_k8s_client(options)
    aiven = Aiven(aiven_project)
    services = [s for s in aiven.get_services() if s.service_type == options.service_type]
    with Progress(console=console, auto_refresh=False) as progress:
        for service in progress.track(services):
            if all(tag in service.tags for tag in ("team", "environment", "tenant")):
                _migrate_service(aiven_project, service, client, options.dry_run)
            else:
                print(f"\n[yellow]Skipping service {service.service_name} because it is missing tags[/yellow]")
            progress.refresh()
