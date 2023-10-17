"""migrate

Uses the Aiven API to identify services of a given type and migrate them to kubernetes resources in the target cluster.

Requires that the [markdown.code]AIVEN_TOKEN[/markdown.code] environment variable be set to a valid Aiven API token.
It is assumed that your kubernetes contexts are named [markdown.code]nav-dev-gcp[/markdown.code]
and [markdown.code]nav-prod-gcp[/markdown.code] for the dev and prod clusters respectively.
"""
import argparse

from rich_argparse import ArgumentDefaultsRichHelpFormatter


def main():
    ArgumentDefaultsRichHelpFormatter.usage_markup = True
    parser = argparse.ArgumentParser(usage=__doc__, formatter_class=ArgumentDefaultsRichHelpFormatter)
    parser.add_argument("env", choices=("dev", "prod"), default="dev", action="store", help="Environment to process")
    parser.parse_args()


if __name__ == '__main__':
    main()
