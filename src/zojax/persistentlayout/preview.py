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
from zope.component import queryUtility
from zojax.statusmessage.interfaces import IStatusMessage

from pt import LayoutPageTemplate
from interfaces import _, ILayoutInformation


class Preview(object):

    def layoutInfo(self):
        layoutId = self.request.get('layoutId')
        info = queryUtility(ILayoutInformation, layoutId)

        if info is None:
            return {'id': layoutId, 'name': None, 'view': None,
                    'context': None, 'layer': None,
                    'title': '', 'description': '', 'template': None}
        else:
            return {'id': layoutId,
                    'name': info.name, 'view': info.view,
                    'context': info.context, 'layer': info.layer,
                    'title': info.layoutclass.title,
                    'description': info.layoutclass.description,
                    'template': info.layoutclass.template}

    def update(self):
        request = self.request

        if 'form.customize' in request:
            id = request.get('layoutId')

            if id in self.context.layouts:
                IStatusMessage(request).add(
                    _(u'Layout already customized.'), 'error')
                return

            info = queryUtility(ILayoutInformation, id)

            if info is None:
                IStatusMessage(request).add(_(u"Can't find layout."), 'error')
                return

            source = info.layoutclass.template.read()

            pt = LayoutPageTemplate()
            pt.source = source

            self.context.setLayout(id, pt)
            IStatusMessage(request).add(_(u'Layout has been customized.'))
            self.redirect('%s/'%id)

        if 'form.back' in request:
            self.redirect('index.html')
