import os
from typing import Optional, Union, Literal

import requests
from pydantic import BaseModel
from rich import get_console, print


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
    dest_project: str
    source_project: str
    source_service: str
    enabled: bool


class User(BaseModel):
    username: str
    type: str


class Service(BaseModel):
    plan: str
    project_vpc_id: Optional[str]
    service_integrations: list[ServiceIntegration]
    service_name: str
    service_type: Union[Literal["kafka"], Literal["opensearch"], Literal["redis"], Literal["influxdb"]]
    service_uri: str
    termination_protection: bool
    users: list[User]


class Aiven(object):
    base = "https://api.aiven.io/v1/project"

    def __init__(self, project, dry_run=False):
        self.project = project
        self.dry_run = dry_run
        self.session = requests.Session()
        self.session.auth = AivenAuth()
        self.base_url = f"{self.base}/{self.project}"

    def get_services(self):
        with get_console().status("Getting services"):
            resp = self.session.get(self.base_url + "/service")
        resp.raise_for_status()
        data = resp.json()
        return [Service.model_validate(s) for s in data["services"]]

    def get_service(self, service):
        with get_console().status("Getting service"):
            resp = self.session.get(self.base_url + f"/service/{service}")
        resp.raise_for_status()
        data = resp.json()
        return Service.model_validate(data["service"])


if __name__ == '__main__':
    aiven = Aiven("nav-dev")
    service = aiven.get_service("opensearch-teampam-stilling")
    print(service)
