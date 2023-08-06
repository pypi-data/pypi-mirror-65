"""
VMware vRealize Workflow implementation and supporting objects.

Copyright (c) 2020, Jose Ibanez

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging
import requests
import time
import six

from .config import URL_RUN_WORKFLOW_BY_ID, SIMPLE_TYPES
from .utils import format_url, safeget


class ParametersError(Exception):
    """Parameters Exception."""
    pass


def parse_value(data):
    """
    >>> data = { "number": { "value": 1.0 } }
    >>> data
    {'number': {'value': 1.0} }
    >>> key, obj = six.next(six.iteritems(data))
    >>> key
    'number'
    >>> obj
    {'value': 1.0}
    >>> value = six.next(six.itervalues(obj))
    >>> value
    1.0
    """

    #print(data)

    if not data:
        return None

    type, obj = six.next(six.iteritems(data))
    value = six.next(six.itervalues(obj))

    # Simple
    if type in SIMPLE_TYPES:
        result = value

    # Array
    elif type == "array":
        result = []
        for e in (value or []):
            result.append(parse_value(e))

    # Properties
    elif type == "properties":
        result = {}
        for e in (value or []):
            key = e.get("key")
            val = parse_value(e.get("value"))
            result[key] = val

    return result



class WorkflowParameter:

    def __init__(self, name=None, value=None, _type=None, scope="local", description=None):
        """
        Returns a new _WorkflowParameter instance.

        :param name: parameter name
        :param value: parameter value
        :param _type: parameter value
        :param scope: parameter scope
        :param description: parameter description
        """
        self.name = name
        self.value = value
        self.type = _type
        self.scope = scope
        self.description = description


    def __str__(self):

        #if self.type in SIMPLE_TYPES or self.type == "Array/string":
        #    return self.name + " = " + str(self.value)
        
        #return self.name + " = <"+self.type+">"
        return self.name + " = " + str(self.value)

    def from_json(self, data):
        """
        Read a parameter from REST wf run answer
        """
        self.name = data.get('name')
        self.scope = data.get('scope')
        self.type = data.get('type')
        self.description = data.get("description")

        if self.type == "String":
            self.type = "string"

        self.value = parse_value(data.get('value'))

        #if self.type in SIMPLE_TYPES:
        #    self.value = safeget(data, 'value', self.type, 'value')
        #
        #elif self.type == "Array/string":
        #    self.value = []
        #
        #    eList = safeget(data, 'value', 'array', 'elements')
        #    if eList is None:
        #        eList = []
        #
        #    for e in eList:
        #        v = safeget(e, 'string', 'value')
        #        self.value.append(v)
        #else:
        #    self.value = "<no suported>" 




    def to_json(self):

        data = {
            "name" : self.name,
            "type" : self.type,
            "scope" : self.scope,
        }

        if self.type in SIMPLE_TYPES:

            value = { "value" : { self.type : { "value": self.value } } }
            data.update(value)


        elif self.type == "Array/string":

            els = []
            for v in self.value:
                els.append({ 'string' : { 'value' : v } })

            value = {  'value' : { 'array' : { 'elements' : els } } }    
            data.update(value)


        else:

            value = { 'value': "<No suported>" }
            data.update(value)


        return data

