# -*- coding: utf-8 -*-
from collective.volto.cookieconsent import _
from collective.volto.cookieconsent.interfaces import ICookieConsentSettings
from plone.app.registry.browser import controlpanel


class CookieConsentSettingsForm(controlpanel.RegistryEditForm):

    schema = ICookieConsentSettings
    label = _(
        'cookie_consent_settings_label', default='Cookie Consent Settings'
    )
    description = _(
        'cookie_consent_settings_help',
        default='Configure cookie consent banner.',
    )


class CookieConsentSettings(controlpanel.ControlPanelFormWrapper):
    form = CookieConsentSettingsForm
