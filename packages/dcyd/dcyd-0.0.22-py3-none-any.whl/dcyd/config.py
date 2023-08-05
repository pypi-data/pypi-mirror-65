import argparse
from halo import Halo
import json
import os
import requests
import sys

import dcyd.utils.constants as constants

def parse_args():
    parser = argparse.ArgumentParser(description='Configure client to communicate with dcyd.')
    parser.add_argument(
        'project_id',
        metavar='project-key',
        help='alphanumeric project identifier (found in the web app)'
    )
    parser.add_argument(
        '-o', '--output-file',
        dest='output_file',
        default=constants.CONFIG_FILE,
        help='output config file name (default: {})'.format(constants.CONFIG_FILE)
    )

    return parser.parse_args()


def configure_client(project_id, config_file):
    with Halo(
            text="Configuring client for project `{}`....".format(project_id),
            interval=150
    ):
        # Call the config service.
        r = requests.post(
            os.path.join(constants.DCYD_API_URL, constants.CONFIG_ROUTE),
            json={'project_id': project_id}
        )

    # Save the config data. We add prefix `mpm_` to distinguish it from the
    # GCP project_id--which is totally internal.
    config = r.json()
    config.update({'mpm_project_id': project_id})

    # Save config file locally.
    with open(config_file, 'w') as f:
        json.dump(config, f)

    print(
        "Client config file `{}` generated successfully.".format(config_file)
    )

def main():
    """Calls the config service to get credentials."""
    with open('dcyd/static/dcyd-ascii-art.txt', 'r') as ascii_art:
        print(ascii_art.read())

    args = parse_args()

    configure_client(args.project_id, args.output_file)

    print("As a final step, run `export {}={}`.".format(
            constants.DCYD_CONFIG_ENV_VAR, args.output_file
        )
    )
