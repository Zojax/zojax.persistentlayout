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
from zope import interface
from BTrees.OOBTree import OOBTree
from zope.location import LocationProxy
from zope.publisher.interfaces import NotFound
from z3c.traverser.interfaces import ITraverserPlugin

from interfaces import _, IPersistentLayoutExtension


class PersistentLayoutExtension(object):
    interface.implements(IPersistentLayoutExtension)

    @property
    def layouts(self):
        """ unset by default """
        layouts = self.data.get('layouts')
        if layouts is None:
            layouts = OOBTree()
            self.data['layouts'] = layouts

        return layouts

    def getLayout(self, id):
        """ get custom layout """
        try:
            layouts = self.data.get('layouts')
            if layouts is None:
                return None
            else:
                return layouts.get(id)
        except:
            return None

    def setLayout(self, id, layout):
        self.layouts[id] = layout

    def removeLayout(self, id):
        layout = self.getLayout(id)
        if layout is not None:
            del self.layouts[id]


class TraverserPlugin(object):
    interface.implements(ITraverserPlugin)

    def __init__(self, container, request):
        self.context = container
        self.request = request

    def publishTraverse(self, request, name):
        try:
            subob = self.context.getLayout(name)
        except:
            subob = None

        if subob is None:
            raise NotFound(self.context, name, request)

        return LocationProxy(subob, self.context, name)
