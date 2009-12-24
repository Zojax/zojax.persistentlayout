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
from zope.proxy import removeAllProxies
from zope.component import queryUtility, getUtilitiesFor
from zope.app.component.interfaces import ISite
from zojax.statusmessage.interfaces import IStatusMessage

from interfaces import _, ILayoutInformation


class ExtensionView(object):

    def layouts(self):
        request = self.request
        context = self.context.context

        customized = self.context.layouts

        names = {}
        layers = list(interface.providedBy(request).flattened())

        layoutsData = {}
        for name, info in getUtilitiesFor(ILayoutInformation):
            if name in customized:
                continue

            if info.layer in layers:
                data = layoutsData.setdefault(info.name, [])
                data.append((layers.index(info.layer), name, info))

        layouts = []
        for name, data in layoutsData.items():
            data.sort()

            info = data[0][2]

            if info.context not in (ISite, interface.Interface) and \
                    issubclass(info.context, interface.Interface):
                if not info.context.providedBy(context):
                    continue

            layouts.append((info.name, data[0][1],
                            {'id': data[0][1],
                             'name': info.name,
                             'view': info.view,
                             'context': info.context,
                             'layer': info.layer,
                             'title': info.layoutclass.title,
                             'description': info.layoutclass.description,
                             }))
        layouts.sort()
        return [info for n, i, info in layouts]

    def customized(self):
        request = self.request
        context = self.context.context

        layouts = []
        for name, pt in self.context.layouts.items():
            info = queryUtility(ILayoutInformation, name)

            if info is None:
                layouts.append((name, name,
                                {'id': name, 'name': None, 'view': None,
                                 'context': None, 'layer': None,
                                 'title': '', 'description': ''}))
            else:
                layouts.append((info.name, name,
                                {'id': name,
                                 'name': info.name, 'view': info.view,
                                 'context': info.context, 'layer': info.layer,
                                 'title': info.layoutclass.title,
                                 'description': info.layoutclass.description}))

        layouts.sort()
        return [info for n, i, info in layouts]

    def update(self):
        request = self.request

        if 'form.button.remove' in request:
            ids = request.get('layoutId')
            if isinstance(ids, basestring):
                ids = (ids,)

            for id in ids:
                self.context.removeLayout(id)
