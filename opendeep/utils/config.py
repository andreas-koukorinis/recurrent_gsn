"""
.. module:: config_tools

Methods used for parsing various configurations (dictionaries, json, yaml, etc.)
"""
__authors__ = "Markus Beissinger"
__copyright__ = "Copyright 2015, Vitruvian Science"
__credits__ = ["Markus Beissinger"]
__license__ = "Apache"
__maintainer__ = "OpenDeep"
__email__ = "dev@opendeep.org"

# standard libraries
import logging
import collections
import os
import json
# third-party libraries
# check if pyyaml is installed
try:
    import yaml
    has_pyyaml = True
except ImportError, e:
    has_pyyaml = False

log = logging.getLogger(__name__)

def create_dictionary_like(input):
    """
    This takes in either an object or filename and parses it into a dictionary. Mostly useful for parsing JSON or YAML config files,
    and returning the dictionary representation.

    :param input: Dictionary-like object (implements collections.Mapping), JSON filename, or YAML filename.
    :type input: collections.Mapping or String

    :return: the parsed dictionary-like object, or None if it could not be parsed.
    :rtype: collections.Mapping or None

    :note: YAML is parsed by the pyyaml library, which would be an optional dependency. Install with 'pip install pyyaml' if you want
    YAML-parsing capabilities.
    """
    if input is None:
        log.warning('Config was None.')
        return None
    # check if it is a dictionary-like object (implements collections.Mapping)
    elif isinstance(input, collections.Mapping):
        return input
    # otherwise, check if it is a filename to a .json or .yaml
    elif os.path.isfile(input):
        _, extension = os.path.splitext(input)
        # if ends in .json
        if extension.lower() is '.json':
            with open(input, 'r') as json_data:
                return json.load(json_data)
        # if ends in .yaml
        elif (extension.lower() is '.yaml' or extension.lower() is '.yml') and has_pyyaml:
            with open(input, 'r') as yaml_data:
                return yaml.load(yaml_data)
        else:
            log.critical('Configuration file %s with extension %s not supported', str(input), extension)
            if not has_pyyaml:
                log.critical('Please install pyyaml with "pip install pyyaml" to parse yaml files.')
            return None
    # otherwise not recognized/supported:
    else:
        log.critical('Could not find config. Either was not collections.Mapping object or not found in filesystem.')
        return None

