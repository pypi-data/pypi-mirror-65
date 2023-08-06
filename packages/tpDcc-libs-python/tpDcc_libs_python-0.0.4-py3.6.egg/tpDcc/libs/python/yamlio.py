#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility methods related to write/read YAML files
"""


from __future__ import print_function, division, absolute_import

import os
import yaml

import yamlordereddictloader

from tpDcc.libs import python


def write_to_file(data, filename, **kwargs):

    """
    Writes data to JSON file
    """

    if '.yml' not in filename:
        filename += '.yml'

    indent = kwargs.pop('indent', 2)

    try:
        with open(filename, 'w') as yaml_file:
            yaml.safe_dump(data, yaml_file, indent=indent, **kwargs)
    except IOError:
        python.logger.error('Data not saved to file {}'.format(filename))
        return None

    python.logger.info('File correctly saved to: {}'.format(filename))

    return filename


def read_file(filename, maintain_order=False):

    """
    Get data from JSON file
    """

    if os.stat(filename).st_size == 0:
        return None
    else:
        try:
            with open(filename, 'r') as yaml_file:
                if maintain_order:
                    data = yaml.load(yaml_file, Loader=yamlordereddictloader.Loader)
                else:
                    data = yaml.safe_load(yaml_file)
        except Exception as err:
            python.logger.warning('Could not read {0}'.format(filename))
            raise err

    return data
