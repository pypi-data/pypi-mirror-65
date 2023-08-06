from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
import logging
import re

from six import text_type

from pyforce.common import bool_
from pyforce.xmlclient import _tSObjectNS

logger = logging.getLogger(__name__)

dateregx = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
datetimeregx = re.compile(
    r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(\.\d+)(.*)'
)

doubleregx = re.compile(r'^(\d)+(\.\d+)?$')

stringtypes = ('string', 'id', 'phone', 'url', 'email',
               'anyType', 'picklist', 'reference', 'encryptedstring')

texttypes = ('textarea')

doubletypes = ('double', 'currency', 'percent')

multitypes = ('combobox', 'multipicklist')

dicttypes = ('address')

_marshallers = dict()


def marshall(fieldtype, fieldname, xml, ns=_tSObjectNS):
    m = _marshallers[fieldtype]
    return m(fieldname, xml, ns)


def register(fieldtypes, func):
    if not isinstance(fieldtypes, (list, tuple, dict)):
        fieldtypes = [fieldtypes]
    for t in fieldtypes:
        _marshallers[t] = func


def stringMarshaller(fieldname, xml, ns):
    return text_type(xml[getattr(ns, fieldname)])


register(stringtypes, stringMarshaller)


def textMarshaller(fieldname, xml, ns):
    # Avoid removal of newlines.
    return stringMarshaller(fieldname, xml, ns)


register(texttypes, textMarshaller)


def multiMarshaller(fieldname, xml, ns):
    asString = text_type(xml[getattr(ns, fieldname), ][0])
    if not asString:
        return []
    return asString.split(';')


register(multitypes, multiMarshaller)


def booleanMarshaller(fieldname, xml, ns):
    return bool_(xml[getattr(ns, fieldname)])


register('boolean', booleanMarshaller)


def integerMarshaller(fieldname, xml, ns):
    strVal = text_type(xml[getattr(ns, fieldname)])
    try:
        i = int(strVal)
        return i
    except:
        return None


register('int', integerMarshaller)


def doubleMarshaller(fieldname, xml, ns):
    strVal = text_type(xml[getattr(ns, fieldname)])
    try:
        i = float(strVal)
        return i
    except:
        return None


register(doubletypes, doubleMarshaller)


def dateMarshaller(fieldname, xml, ns):
    datestr = text_type(xml[getattr(ns, fieldname)])
    match = dateregx.match(datestr)
    if match:
        grps = match.groups()
        year = int(grps[0])
        month = int(grps[1])
        day = int(grps[2])
        return datetime.date(year, month, day)
    return None


register('date', dateMarshaller)


def dateTimeMarshaller(fieldname, xml, ns):
    datetimestr = text_type(xml[getattr(ns, fieldname)])
    match = datetimeregx.match(datetimestr)
    if match:
        grps = match.groups()
        year = int(grps[0])
        month = int(grps[1])
        day = int(grps[2])
        hour = int(grps[3])
        minute = int(grps[4])
        second = int(grps[5])
        secfrac = float(grps[6])
        microsecond = int(secfrac * (10**6))
        tz = grps[7]  # XXX not sure if I need to do anything with this. sofar
        # times appear to be UTC
        return datetime.datetime(
            year, month, day, hour, minute, second, microsecond
        )
    return None


register('datetime', dateTimeMarshaller)


def base64Marshaller(fieldname, xml, ns):
    return text_type(xml[getattr(ns, fieldname)])


register('base64', base64Marshaller)


def dictMarshaller(fieldname, xml, ns):
    mydict = {}
    for key in xml[getattr(ns, fieldname)]:
        mydict[key._name[1]] = key.__str__()
    return mydict


register(dicttypes, dictMarshaller)
