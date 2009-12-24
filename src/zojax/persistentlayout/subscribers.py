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
from zope import component
from zojax.layout.interfaces import ILayoutCreatedEvent, ILayoutTemplateFile

from interfaces import ILayoutInformation
from information import LayoutInformation
from template import CustomizableLayoutTemplateFile


@component.adapter(ILayoutCreatedEvent)
def newLayoutCreated(event):
    return
    layoutclass = event.layoutclass

    # we can customize only ILayoutTemplateFile template
    if not ILayoutTemplateFile.providedBy(layoutclass.template):
        return

    # layout information
    info = LayoutInformation(
        event.uid, event.name, event.view,
        event.context, event.layer, event.layoutclass)
    sm = component.getSiteManager()
    sm.registerUtility(info, ILayoutInformation, name=event.uid)

    # create customizable template
    template = CustomizableLayoutTemplateFile.__new__(
        CustomizableLayoutTemplateFile)
    template.__dict__.update(layoutclass.template.__dict__)
    template.information = info

    layoutclass.template = template
