# -*- coding: utf-8 -*-
from collective.volto.cookieconsent.interfaces import ICookieConsentSettings
from collective.volto.cookieconsent.testing import (
    VOLTO_COOKIECONSENT_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from transaction import commit

import json
import unittest


class SocialInfosTest(unittest.TestCase):

    layer = VOLTO_COOKIECONSENT_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_route_exists(self):
        response = self.api_session.get("/@cookieconsent-infos")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Content-Type"), "application/json"
        )

    def tearDown(self):
        self.api_session.close()

    def test_return_empty_infos_if_not_set(self):
        response = self.api_session.get("/@cookieconsent-infos")
        results = response.json()

        self.assertEqual(
            results,
            {'accept_on_scroll': False, 'cookie_consent_configuration': {}},
        )

    def test_right_data(self):
        api.portal.set_registry_record(
            'accept_on_scroll', True, interface=ICookieConsentSettings
        )
        api.portal.set_registry_record(
            'cookie_consent_configuration',
            json.dumps({'foo': 'bar'}),
            interface=ICookieConsentSettings,
        )
        commit()
        response = self.api_session.get("/@cookieconsent-infos")
        results = response.json()

        self.assertEqual(
            results,
            {
                'accept_on_scroll': True,
                'cookie_consent_configuration': {'foo': 'bar'},
            },
        )
