# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.volto.cookieconsent.testing import (
    VOLTO_COOKIECONSENT_INTEGRATION_TESTING,
)  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.volto.cookieconsent is properly installed."""

    layer = VOLTO_COOKIECONSENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.volto.cookieconsent is installed."""
        self.assertTrue(
            self.installer.isProductInstalled('collective.volto.cookieconsent')
        )
        self.assertTrue(self.installer.isProductInstalled('plone.restapi'))

    def test_browserlayer(self):
        """Test that ICollectiveVoltoCookieConsentLayer is registered."""
        from collective.volto.cookieconsent.interfaces import (
            ICollectiveVoltoCookieConsentLayer,
        )
        from plone.browserlayer import utils

        self.assertIn(
            ICollectiveVoltoCookieConsentLayer, utils.registered_layers()
        )


class TestUninstall(unittest.TestCase):

    layer = VOLTO_COOKIECONSENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.volto.cookieconsent'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.volto.cookieconsent is cleanly uninstalled."""
        self.assertFalse(
            self.installer.isProductInstalled('collective.volto.cookieconsent')
        )

    def test_browserlayer_removed(self):
        """Test that ICollectiveVoltoCookieConsentLayer is removed."""
        from collective.volto.cookieconsent.interfaces import (
            ICollectiveVoltoCookieConsentLayer,
        )
        from plone.browserlayer import utils

        self.assertNotIn(
            ICollectiveVoltoCookieConsentLayer, utils.registered_layers()
        )
