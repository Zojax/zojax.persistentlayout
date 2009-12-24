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
from StringIO import StringIO

from threading import local
from zope.proxy import removeAllProxies
from zope.component import queryMultiAdapter
from zope.traversing.namespace import view
from zope.app.component.hooks import getSite
from zope.tal.talinterpreter import TALInterpreter
from zope.pagetemplate.interfaces import IPageTemplate
from zojax.layout.layout import LayoutTemplateFile

from interfaces import IPersistentLayoutExtension


class CustomizableLayoutTemplateFile(LayoutTemplateFile):

    expand = False

    def pt_render(self, namespace, source=False,
                  sourceAnnotations=False, showtal=False):
        """Render this Page Template"""
        layout = namespace['layout']

        program = self._get_custom_tal(layout, namespace['maincontext'])

        if program is None:
            program = self._get_custom_tal(layout, namespace['layoutcontext'])

        if program is None:
            site = getSite()
            if site is not namespace['layoutcontext']:
                program = self._get_custom_tal(layout, site)

        if program is None:
            return super(LayoutTemplateFile, self).pt_render(
                namespace, source, sourceAnnotations, showtal)

        program = removeAllProxies(program)

        output = StringIO(u'')
        context = self.pt_getEngineContext(namespace)

        TALInterpreter(program, {},
                       context, output, tal=not source, showtal=showtal,
                       strictinsert=0, sourceAnnotations=sourceAnnotations)()
        return output.getvalue()

    def _get_custom_tal(self, layout, context):
        if not layoutProcessing.process:
            return

        extension = IPersistentLayoutExtension(context, None)
        if extension is None:
            return

        tal = extension.getLayout(self.information.uid)

        if tal is not None and tal.program is not None:
            return tal.program


class LayoutPrcessing(local):

    process = True

layoutProcessing = LayoutPrcessing()


class NoPersistentLayouts(view):

    def traverse(self, name, ignored):
        self.request.shiftNameToApplication()
        layoutProcessing.process = False
        return self.context


class YesPersistentLayouts(view):

    def traverse(self, name, ignored):
        self.request.shiftNameToApplication()
        layoutProcessing.process = True
        return self.context
