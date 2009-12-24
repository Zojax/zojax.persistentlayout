##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import sys
from zope import interface
from persistent import Persistent

from zope.tal.talgenerator import TALGenerator
from zope.tal.htmltalparser import HTMLTALParser
from zope.app.pagetemplate.engine import TrustedEngine

from interfaces import ICustomLayoutTemplate


class LayoutPageTemplate(Persistent):
    interface.implements(ICustomLayoutTemplate)

    _source = u''
    errors = ()

    _v_errors = ()
    _v_program = None

    enabled = True

    def _get_source(self):
        return self._source

    def _set_source(self, source):
        self._source = source
        self._cook()

        if self._v_errors:
            self.errors = self._v_errors
        else:
            self.errors = ()

    source = property(_get_source, _set_source)

    def _cook(self):
        self._v_program = None

        if not self._source:
            return

        parser = HTMLTALParser(TALGenerator(TrustedEngine))
        try:
            parser.parseString(self.source)
            self._v_program, macros = parser.getCode()
            self._v_errors = ()
        except Exception, e:
            self._v_program = None
            self._v_errors = [unicode(err) for err in sys.exc_info()[:2]]

    @property
    def program(self):
        if not self.enabled:
            return None

        if self._v_program is None:
            self._cook()
            return self._v_program

        return self._v_program
