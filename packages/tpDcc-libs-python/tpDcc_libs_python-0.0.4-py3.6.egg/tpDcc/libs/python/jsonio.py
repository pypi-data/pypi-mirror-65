#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility methods related to write/read json files
"""


from __future__ import print_function, division, absolute_import

import os
import json

from tpDcc.libs import python


def write_to_file(data, filename, **kwargs):

    """
    Writes data to JSON file
    """

    if '.json' not in filename:
        filename += '.json'

    indent = kwargs.pop('indent', 2)

    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=indent, **kwargs)
    except IOError:
        python.logger.error('Data not saved to file {}'.format(filename))
        return None

    python.logger.info('File correctly saved to: {}'.format(filename))

    return filename


def read_file(filename):

    """
    Get data from JSON file
    """

    if os.stat(filename).st_size == 0:
        return None
    else:
        try:
            with open(filename, 'r') as json_file:
                data = json.load(json_file)
        except Exception as err:
            python.logger.warning('Could not read {0}'.format(filename))
            raise err

    return data
