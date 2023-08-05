#!/usr/bin/env python3

from functools import wraps
import datetime as dt
import inspect
import json
import logging
import uuid

from dcyd.utils.async_logger import async_logger
import dcyd.utils.constants as constants
from dcyd.utils.utils import (
    get_gcp_project_id,
    get_project_id,
    get_mpm_client_data,
    make_json_serializable
)

logger = async_logger()

def mpm(func=None, **custom_kwargs):
    '''Decorator factory

    Including the initial argument "func" is a trick necessary to make this
    decorator optionally callable without args, as in: @mpm
    '''
    def decorator(func):
        """Decorator that logs function inputs and outputs
        """
        @wraps(func)
        def wrapper(*args, **kwargs):

            # Record request timestamp
            req_ts = dt.datetime.utcnow().isoformat()

            # Call the actual function.
            response = func(*args, **kwargs)

            # Form and send response payload to dcyd.
            payload = format_payload(
                func, args, kwargs, custom_kwargs, req_ts, response
            )
            logger.info(constants.MPM_LOG_MSG, payload)

            # Send expected response to function caller.
            return response

        return wrapper

    if func:
        return decorator(func)

    return decorator


def format_payload(
        func, func_args, func_kwargs, custom_kwargs, req_ts, response
):
    """
    Args:
        func:
        func_args:
        func_kwargs:
        custom_args:
        req_ts (str):
        response:
    """
    # bind arguments
    ba = inspect.signature(func).bind(*func_args, **func_kwargs)
    ba.apply_defaults()

    """If func is a method, its first argument is the class it belongs to, which
    needs to be excised since it isn't json serializable.

    We infer that func is a method if func's name is an attribute of the first
    argument. This is compelling but not airtight."""

    if ba.arguments and hasattr(list(ba.arguments.values())[0], func.__name__):
        ba.arguments.popitem(last=False)
        function_type = 'method'
    else:
        function_type = 'function'

    payload = {
        'function': {
            'function_name': func.__name__,
            'function_qualname': func.__qualname__,
            'function_module': func.__module__,
            'function_sourcefile': inspect.getsourcefile(func),
            'function_type': function_type,
            'function_environment': custom_kwargs.pop(
                'environment', constants.DEFAULT_ENVIRONMENT
            )
        },
        'request': {
            'request_id': str(uuid.uuid4()),
            'request_timestamp': req_ts,
            'request_arguments': make_json_serializable(ba.arguments),
            'request_parameters': {
                k: str(v.kind) for k, v in ba.signature.parameters.items()
            },
            'request_response': make_json_serializable(response),
            'request_response_timestamp': dt.datetime.utcnow().isoformat()
        },
        'project_id': get_project_id(),
        'mpm_client': get_mpm_client_data(),
        'custom_data': make_json_serializable(custom_kwargs),
    }

    return payload
