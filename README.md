aiven-iac-migration
===================

A tool to migrate Aiven services from Terraform to using the Aiven Operator in kubernetes.

Uses the Aiven API to discover services of a given type, and creates corresponding resources in a kubernetes cluster.
Does not currently manage terraform state, so terraform clean up must be performed manually when done.

## Usage

To get started you need poetry and Python 3.11 installed.

Then run the following commands:
```
poetry install
poetry run migrate --help
```
