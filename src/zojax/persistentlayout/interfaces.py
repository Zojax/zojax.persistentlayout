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
from zope import schema, interface
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zojax.persistentlayout')


class IPersistentLayoutExtension(interface.Interface):

    layouts = interface.Attribute('Layouts')

    def getLayout(id):
        """ get custom layout """

    def setLayout(id, layout):
        """ set layout """

    def removeLayout(id):
        """ remove layout """


class ICustomLayoutTemplate(interface.Interface):
    """ pagetemplate for layout """

    enabled = schema.Bool(
        title = _('Enabled'),
        required = False)

    source = schema.SourceText(
        title = _('Source'),
        description = _('The source of the layout page template.'),
        required = True)

    errors = interface.Attribute('Errors')


class ILayoutInformation(interface.Interface):
    """ information about registered layout """

    name = interface.Attribute('Name')

    view = interface.Attribute('View')

    context = interface.Attribute('Context')

    layer = interface.Attribute('Layer')

    layoutclass = interface.Attribute('Generated class for layout')
