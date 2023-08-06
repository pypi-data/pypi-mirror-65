# -*- coding: utf-8 -*-
from spaceone.core.error import *


class ERROR_NOT_ALLOW_PINNING_KEYS(ERROR_INVALID_ARGUMENT):
    _message = 'Pinning keys not allowed. (key={key})'


class ERROR_INVALID_METADATA_KEY(ERROR_INVALID_ARGUMENT):
    _message = 'The metadata key only allows details and sub_data.'


class ERROR_METADATA_LIST_VALUE_TYPE(ERROR_INVALID_ARGUMENT):
    _message = 'The value of metadata\'s {key} must be a list type.'
