# -*- coding: utf-8 -*-
from collective.volto.cookieconsent.interfaces import ICookieConsentSettings
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface


@adapter(Interface, Interface)
class CookieConsentSettingsControlpanel(RegistryConfigletPanel):
    schema = ICookieConsentSettings
    configlet_id = "CookieConsentSettings"
    configlet_category_id = "plone-general"
    schema_prefix = None
