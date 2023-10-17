"""migrate

Uses the Aiven API to identify services of a given type and migrate them to kubernetes resources in the target cluster.

Requires that the [markdown.code]AIVEN_TOKEN[/markdown.code] environment variable be set to a valid Aiven API token.
It is assumed that your kubernetes contexts are named [markdown.code]nav-dev-gcp[/markdown.code]
and [markdown.code]nav-prod-gcp[/markdown.code] for the dev and prod clusters respectively.
"""
import argparse

from rich import traceback
from rich.console import Console
from rich.text import Text
from rich_argparse import ArgumentDefaultsRichHelpFormatter

from .migrate import migrate
from . import errors

# PLAN OF ATTACK
# * Get all services of requested type
# * For each service:
#   * Parse tags to find team
#   * Create Aiven resource in team namespace
#   * Create ServiceIntegration for prometheus metrics in team namespace


def main():
    ArgumentDefaultsRichHelpFormatter.usage_markup = True
    parser = argparse.ArgumentParser(usage=__doc__, formatter_class=ArgumentDefaultsRichHelpFormatter)
    parser.add_argument("env", choices=("dev", "prod"), nargs="?", default="dev", action="store", help="Environment to process")
    parser.add_argument("service_type", choices=("opensearch",), nargs="?", default="opensearch", action="store", help="Service type to process")
    options = parser.parse_args()
    console = Console()
    traceback.install(console=console)
    try:
        migrate(options)
    except errors.MigrateError as e:
        output = Text(str(e), style="bold red")
        if e.__cause__:
            output.append(Text(":\n\t"))
            output.append(Text(str(e.__cause__), style="red"))
        console.print(output)
        exit(1)


if __name__ == '__main__':
    main()
