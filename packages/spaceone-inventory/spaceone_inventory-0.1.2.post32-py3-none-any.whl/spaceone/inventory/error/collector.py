# -*- coding: utf-8 -*-
from spaceone.core.error import *

class ERROR_NO_COLLECTOR(ERROR_BASE):
    _message = '{collector_id} does not exist in {domain_id}'

class ERROR_VERIFY_PLUGIN_FAILURE(ERROR_BASE):
    _message = 'Fail to verify plugin, params={params}'

class ERROR_NO_PLUGIN_PARAMETER(ERROR_BASE):
    _message = 'parameter: {param} is required'

class ERROR_TOKEN_AUTHENTICATION_FAILURE(ERROR_BASE):
    _message = 'A access token or refresh token is invalid.'

class ERROR_AUTHENTICATION_FAILURE_PLUGIN(ERROR_BASE):
    _message = 'External plugin authentication exception. (plugin_error_message={message})'

class ERROR_JOB_STATE_CHANGE(ERROR_BASE):
    _message = 'Job {job_id} state change: {state} -> {action}'

class ERROR_COLLECT_FILTER(ERROR_BASE):
    _message = 'collect failed, plugin_info: {plugin_info}, filter: {param}'

class ERROR_COLLECTOR_SECRET(ERROR_BASE):
    _message = 'collect failed, plugin_info: {plugin_info}, secret_id: {param}'

class ERROR_JOB_UPDATE(ERROR_BASE):
    _message = 'job update failed, param={param}'

class ERROR_COLLECTOR_COLLECTING(ERROR_BASE):
    _message = 'collecting failed, plugin_info: {plugin_info}, filter: {filter}'

class ERROR_COLLECT_CANCELED(ERROR_BASE):
    _message = 'collecting canceled, job_id: {job_id}'

class ERROR_UNSUPPORTED_RESOURCE_TYPE(ERROR_BASE):
    _message = 'collector can not find resource_type: {resource_type}'

class ERROR_UNSUPPORTED_FILTER_KEY(ERROR_BASE):
    _message = 'request unsupported filter_key {filter_key} : {filter_value}'
