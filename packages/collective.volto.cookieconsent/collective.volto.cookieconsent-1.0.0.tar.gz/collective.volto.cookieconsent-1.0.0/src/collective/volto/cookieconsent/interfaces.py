# -*- coding: utf-8 -*-
from collective.volto.cookieconsent import _
from zope.interface import Interface
from zope.interface import Invalid
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import Bool, SourceText

import json


def validate_cfg_json(value):
    """check that we have at least valid json and its a dict
    """
    try:
        jv = json.loads(value)
    except ValueError as e:
        raise Invalid(
            _(
                'invalid_json',
                'JSON is not valid, parser complained: ${message}',
                mapping={'message': e.message},
            )
        )
    if not isinstance(jv, dict):
        raise Invalid(
            _('invalid_cfg_no_dict', 'JSON root must be a mapping (dict)')
        )
    return True


class ICollectiveVoltoCookieConsentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICookieConsentSettings(Interface):
    """ Interface for cookie consent controlpanel """

    accept_on_scroll = Bool(
        title=_(
            'accept_on_scroll_label', default='Accept policy on scroll'
        ),
        description=_(
            'accept_on_scroll_help',
            default='If checked, scrolling the page will be interrpreted'
                    ' as the user accepted the cookie policy.',
        ),
    )

    cookie_consent_configuration = SourceText(
        title=_(
            'cookie_consent_configuration_label',
            default='Cookie consent configuration',
        ),
        description=_(
            'cookie_consent_configuration_help',
            default='Provide a configuration of the cookie consent banner.'
            'You can set different configurations for each enabled language.'
            'The first defined policy configuration will be the default one '
            '(the one used when not language specific configuration is found).',  # noqa
        ),
        default='{}',
        required=True,
        constraint=validate_cfg_json,
    )
