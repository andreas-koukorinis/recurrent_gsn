"""
.. module:: misc

This module contains utils that are general and can't be grouped logically into the other opendeep.utils modules.
"""
__authors__ = "Markus Beissinger"
__copyright__ = "Copyright 2015, Vitruvian Science"
__credits__ = ["Markus Beissinger"]
__license__ = "Apache"
__maintainer__ = "OpenDeep"
__email__ = "dev@opendeep.org"

# standard libraries
import logging
# third party libraries
import numpy
import theano
import theano.tensor as T
# internal imports
from opendeep import trunc

log = logging.getLogger(__name__)

def make_time_units_string(time):
    """
    This takes a time (in seconds) and converts it to an easy-to-read format with the appropriate units.

    :param time: the time to make into a string (in seconds)
    :type time: Integer

    :return: an easy-to-read string representation of the time
    :rtype: String
    """
    # Show the time with appropriate units.
    if time < 0:
        return trunc(time*1000)+" milliseconds"
    elif time < 60:
        return trunc(time)+" seconds"
    elif time < 3600:
        return trunc(time/60)+" minutes"
    else:
        return trunc(time/3600)+" hours"
    
def raise_to_list(_input):
    """
    This will take an input and raise it to a List (if applicable)

    :param _input: object to raise to a list
    :type _input: Object

    :return: the object as a list, or none
    :rtype: List or None
    """
    if _input is None:
        return None
    elif isinstance(_input, list):
        return _input
    else:
        return [_input]
    
def stack_and_shared(_input):
    """
    This will take a list of input variables, turn them into theano shared variables, and return them stacked in a single tensor.

    :param _input: list of input variables
    :type _input: list, object, or none

    :return: symbolic tensor of the input variables stacked, or none
    :rtype: Tensor or None
    """
    if _input is None:
        return None
    elif isinstance(_input, list):
        shared_ins = []
        for _in in _input:
            try:
                shared_ins.append(theano.shared(_in))
            except TypeError as _:
                shared_ins.append(_in)
        return T.stack(shared_ins)
    else:
        try:
            _output = [theano.shared(_input)]
        except TypeError as _:
            _output = [_input]
        return T.stack(_output)
    
def concatenate_list(input, axis=0):
    """
    This takes a list of tensors and concatenates them along the axis specified (0 by default)

    :param input: list of tensors
    :type input: List

    :param axis: axis to concatenate along
    :type axis: Integer

    :return: the concatenated tensor, or None
    :rtype: Tensor or None
    """
    if input is None:
        return None
    elif isinstance(input, list):
        return T.concatenate(input, axis=axis)
    else:
        return input
    
    
def closest_to_square_factors(n):
    """
    This function finds the integer factors that are closest to the square root of a number. (Useful for finding the closest
    width/height of an image you want to make square)

    :param n: The number to find its closest-to-square root factors.
    :type n: Integer

    :return: the tuple of (factor1, factor2) that are closest to the square root
    :rtype: Tuple
    """
    test = numpy.ceil(numpy.sqrt(float(n)))
    while not (n/test).is_integer():
        test-=1
    if test < 1:
        test = 1
    return int(test), int(n/test)