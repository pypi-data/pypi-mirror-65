# -*- coding: utf-8 -*-

import doctest
import unittest
import zope.component

from dolmen.beaker import tests
from zope.component import eventtesting
from zope.component.testlayer import ZCMLFileLayer
from zope.interface import Interface
from zope.interface.interfaces import IComponentLookup
from zope.site.folder import rootFolder
from zope.site.site import LocalSiteManager, SiteManagerAdapter
from zope.traversing.testing import setUp as traversingSetUp


class DolmenBeakerLayer(ZCMLFileLayer):
    """The dolmen.beaker main test layer.
    """

    def setUp(self):
        ZCMLFileLayer.setUp(self)
        eventtesting.setUp()
        traversingSetUp()
        zope.component.hooks.setHooks()

        # Set up site manager adapter
        zope.component.provideAdapter(
            SiteManagerAdapter, (Interface,), IComponentLookup)

        # Set up site
        site = rootFolder()
        site.setSiteManager(LocalSiteManager(site))
        zope.component.hooks.setSite(site)

    def tearDown(self):
        ZCMLFileLayer.tearDown(self)
        zope.component.hooks.resetHooks()
        zope.component.hooks.setSite()


def test_suite():
    suite = unittest.TestSuite()
    readme = doctest.DocFileSuite(
        '../README.txt', globs={'__name__': 'dolmen.beaker.tests'},
        optionflags=(doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE))
    readme.layer = DolmenBeakerLayer(tests)
    cache = doctest.DocFileSuite(
        '../cache.txt', globs={'__name__': 'dolmen.beaker.tests'},
        optionflags=(doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE))
    cache.layer = DolmenBeakerLayer(tests)
    suite.addTest(readme)
    suite.addTest(cache)
    return suite
