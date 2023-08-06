# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.restapi.testing import PloneRestApiDXLayer
from plone.testing import z2


import collective.volto.cookieconsent
import plone.restapi


class VoltoCookieConsentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.volto.cookieconsent)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.volto.cookieconsent:default')


VOLTO_COOKIECONSENT_FIXTURE = VoltoCookieConsentLayer()


VOLTO_COOKIECONSENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VOLTO_COOKIECONSENT_FIXTURE,),
    name='VoltoCookieConsentLayer:IntegrationTesting',
)


VOLTO_COOKIECONSENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VOLTO_COOKIECONSENT_FIXTURE,),
    name='VoltoCookieConsentLayer:FunctionalTesting',
)


VOLTO_COOKIECONSENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        VOLTO_COOKIECONSENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='VoltoCookieConsentLayer:AcceptanceTesting',
)


class VoltoCookieConsentRestApiLayer(PloneRestApiDXLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(VoltoCookieConsentRestApiLayer, self).setUpZope(
            app, configurationContext
        )

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.volto.cookieconsent)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.volto.cookieconsent:default')


VOLTO_COOKIECONSENT_API_FIXTURE = VoltoCookieConsentRestApiLayer()
VOLTO_COOKIECONSENT_API_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VOLTO_COOKIECONSENT_API_FIXTURE,),
    name="VoltoCookieConsentRestApiLayer:Integration",
)

VOLTO_COOKIECONSENT_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VOLTO_COOKIECONSENT_API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="VoltoCookieConsentRestApiLayer:Functional",
)
