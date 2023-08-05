#!/usr/bin/env python3

import base64
import json
import os
import pickle
import pkg_resources

import dcyd.utils.constants as constants


def get_gcp_project_id():
    '''Returns the GCP project_id, found in the key .json file.'''

    with open(os.environ[constants.DCYD_CONFIG_ENV_VAR], 'r') as f:
        config = json.load(f)

    # Use brackets, since I want to raise an error if key not found.
    return config['project_id']


def get_project_id():
    '''Returns the MPM project_id, found in the key .json file.'''
    with open(os.environ[constants.DCYD_CONFIG_ENV_VAR], 'r') as f:
        config = json.load(f)

    # Use brackets, since I want to raise an error if key not found.
    return config['mpm_project_id']


def get_mpm_client_data():
    dist = pkg_resources.get_distribution('dcyd')

    return {
        'mpm_client_name': dist.key,
        'mpm_client_version': dist.version,
        'mpm_client_language': 'python'
    }


def make_json_serializable(obj):
    '''To ensure obj is JSON-serializable, pickle and base64-encode it.

    arg obj: object to be tested for JSON-serializability
    type obj: any Python object

    returns: a transformation of obj that is JSON-serializable.
    '''

    return base64.b64encode( # encode the byte string into bytes
        pickle.dumps(obj) # convert the object into a byte string
    ).decode('ascii')
