import os
from typing import Optional, Union, Literal

import requests
from requests.exceptions import HTTPError
from pydantic import BaseModel
from rich import get_console, print

from migration.errors import AivenError, AivenUnauthenticated


class AivenAuth(requests.auth.AuthBase):
    def __init__(self, token=None):
        if token is None:
            token = os.getenv("AIVEN_TOKEN")
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = f"Bearer {self.token}"
        return r


class ServiceIntegration(BaseModel):
    active: bool
    description: str
    dest_endpoint: Optional[str]
    dest_endpoint_id: Optional[str]
    dest_project: str
    enabled: bool
    integration_type: str
    service_integration_id: str
    source_project: str
    source_service: str


class User(BaseModel):
    username: str
    type: str


class Service(BaseModel):
    cloud_name: str
    disk_space_mb: int
    plan: str
    project_vpc_id: Optional[str]
    service_integrations: list[ServiceIntegration]
    service_name: str
    service_type: Union[Literal["kafka"], Literal["opensearch"], Literal["redis"], Literal["influxdb"]]
    service_uri: str
    termination_protection: bool
    users: list[User]
    tags: dict[str, str]


class Aiven(object):
    base = "https://api.aiven.io/v1/project"

    def __init__(self, project, dry_run=False):
        self.project = project
        self.dry_run = dry_run
        self.session = requests.Session()
        self.session.auth = AivenAuth()
        self.base_url = f"{self.base}/{self.project}"

    def _call_api(self, path, operation="Calling Aiven API"):
        with get_console().status(operation.capitalize()):
            resp = self.session.get(self.base_url + path)
            if resp.status_code == 401:
                raise AivenUnauthenticated("Aiven token is invalid")
            try:
                resp.raise_for_status()
            except HTTPError as e:
                raise AivenError(f"Error when {operation}") from e
            return resp

    def get_services(self):
        resp = self._call_api("/service", "getting services")
        data = resp.json()
        return [Service.model_validate(s) for s in data["services"]]

    def get_service(self, service):
        resp = self._call_api(f"/service/{service}", f"getting service {service}")
        data = resp.json()
        return Service.model_validate(data["service"])


if __name__ == '__main__':
    aiven = Aiven("nav-dev")
    service = aiven.get_service("opensearch-teampam-stilling")
    print(service)
