"""
Conversions to unicode.

Author(s): Arno Bakker
"""
from __future__ import absolute_import

import sys

from six import binary_type, text_type


def ensure_unicode(s, encoding, errors='strict'):
    """Similar to six.ensure_text() except that the encoding parameter is *not* optional
    """
    if isinstance(s, binary_type):
        return s.decode(encoding, errors)
    elif isinstance(s, text_type):
        return s
    else:
        raise TypeError("not expecting type '%s'" % type(s))


def bin2unicode(bin, possible_encoding='utf_8'):
    sysenc = sys.getfilesystemencoding()
    if possible_encoding is None:
        possible_encoding = sysenc
    try:
        return bin.decode(possible_encoding)
    except:
        try:
            if possible_encoding == sysenc:
                raise
            return bin.decode(sysenc)
        except:
            try:
                return bin.decode('utf_8')
            except:
                try:
                    return bin.decode('iso-8859-1')
                except:
                    try:
                        return bin.decode(sys.getfilesystemencoding())
                    except:
                        return bin.decode(sys.getdefaultencoding(), errors='replace')


def str2unicode(s):
    try:
        return text_type(s)
    except UnicodeDecodeError:
        for encoding in [sys.getfilesystemencoding(), 'utf_8', 'iso-8859-1']:
            try:
                return ensure_unicode(s, encoding)
            except UnicodeDecodeError:
                pass
    return None


def dunno2unicode(dunno):
    newdunno = None
    if isinstance(dunno, text_type):
        newdunno = dunno
    else:
        try:
            newdunno = bin2unicode(dunno)
        except:
            newdunno = str2unicode(dunno)
    return newdunno
