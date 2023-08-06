# -*- coding: utf-8 -*-
from collective.volto.cookieconsent.interfaces import ICookieConsentSettings
from plone import api
from plone.restapi.services import Service
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import json


@implementer(IPublishTraverse)
class CookieConsentInfosGet(Service):
    def __init__(self, context, request):
        super(CookieConsentInfosGet, self).__init__(context, request)

    def reply(self):
        accept_on_scroll = (
            api.portal.get_registry_record(
                'accept_on_scroll',
                interface=ICookieConsentSettings,
                default=False,
            )
            or False  # noqa
        )
        cookie_consent_configuration = (
            api.portal.get_registry_record(
                'cookie_consent_configuration',
                interface=ICookieConsentSettings,
                default='{}',
            )
            or '{}'  # noqa
        )

        return {
            'accept_on_scroll': accept_on_scroll,
            'cookie_consent_configuration': json.loads(
                cookie_consent_configuration
            ),
        }
