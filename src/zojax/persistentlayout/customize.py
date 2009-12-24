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
from zope.component import queryUtility, getMultiAdapter

from z3c.form.interfaces import IFieldWidget

from zojax.layoutform import Fields, PageletEditForm
from zojax.statusmessage.interfaces import IStatusMessage

from interfaces import _, ILayoutInformation, ICustomLayoutTemplate


def customWidget(field, request):
    widget = getMultiAdapter((field, request), IFieldWidget)

    widget.rows = 50
    widget.style = u'width: 98%; font-family: monospace; font-size: 130%'

    return widget


class CustomizeView(PageletEditForm):

    fields = Fields(ICustomLayoutTemplate)
    fields['source'].widgetFactory = customWidget

    def cancelURL(self):
        return '../'


class CustomizeViewInfo(object):

    def layoutInfo(self):
        layoutId = self.context.__parent__.__name__
        info = queryUtility(ILayoutInformation, layoutId)

        if info is None:
            return {'id': layoutId,
                    'name': _('No name'), 'view': None,
                    'context': None, 'layer': None,
                    'title': '', 'description': ''}
        else:
            return {'id': layoutId,
                    'name': info.name, 'view': info.view,
                    'context': info.context, 'layer': info.layer,
                    'title': info.layoutclass.title,
                    'description': info.layoutclass.description}
