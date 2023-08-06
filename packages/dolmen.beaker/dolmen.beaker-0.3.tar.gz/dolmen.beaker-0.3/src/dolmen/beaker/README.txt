=============
dolmen.beaker
=============

Session
=======

Configuration
-------------

   >>> from zope.component import getUtility, queryUtility
   >>> from dolmen.beaker.interfaces import ISessionConfig

   >>> session_config = queryUtility(ISessionConfig)
   >>> session_config.get('key')
   'beaker.session.id'


Initialisation
--------------

``dolmen.beaker`` initialize the beaker session when the traversing
starts (traversing the IRootFolder object)::

   >>> from zope.event import notify
   >>> import grokcore.component as grok
   >>> from zope.publisher.browser import TestRequest
   >>> from zope.publisher.interfaces.http import IHTTPRequest
   >>> from zope.traversing.interfaces import BeforeTraverseEvent

First we create an instance of the Request::

   >>> request = TestRequest()
   >>> IHTTPRequest.providedBy(request)
   True

We initalize our Session with the help of the BeforeTraverseEvent.
This event will make an instance of a Session Object in the Request::

   >>> from zope.component.hooks import getSite
   >>> site = getSite()
   >>> notify(BeforeTraverseEvent(site, request))

We can get the session object using two available adapters::

   >>> from dolmen.beaker.interfaces import ISession
   >>> session = ISession(request)
   >>> session.__class__
   <class 'beaker.session.SessionObject'>

Let's assign an value to our session and save it::

   >>> session['foo'] = 'bar'
   >>> session.save()
   >>> session['foo']
   'bar'

A new request will not have access to the session without traversing::

   >>> newrequest = TestRequest()
   >>> newrequest.response._cookies
   {}

   >>> session = ISession(newrequest)
   >>> session['foo']
   Traceback (most recent call last):
   ...
   KeyError: 'foo'


closure and invalidation
------------------------

   >>> cookie = request.response._cookies
   >>> cookie
   {}

   >>> from zope.publisher.interfaces import EndRequestEvent
   >>> notify(EndRequestEvent(site, request))

   >>> cookie = request.response._cookies
   >>> cookie
   {'beaker.session.id': {'path': '/', 'samesite': 'Lax', 'value': '...'}}

Invalidating
------------

   >>> import hamcrest
   >>> session = ISession(request)
   >>> print(session['foo'])
   bar

   >>> session.invalidate() # Or destroy, to get rid of everything
   >>> session['foo']
   Traceback (most recent call last):
   ...
   KeyError: 'foo'


The Zope Session adapter
========================

   >>> from zope.session.interfaces import ISession as IZopeSession

   >>> request = TestRequest()
   >>> notify(BeforeTraverseEvent(site, request))

   >>> zsession = IZopeSession(request)
   >>> print(zsession)
   <dolmen.beaker.session.ZopeSession object at ...>

   >>> from zope.interface.verify import verifyObject
   >>> verifyObject(IZopeSession, zsession)
   True

   >>> data = zsession['my_package']
   >>> print(data)
   <dolmen.beaker.session.NamespaceSessionData object at ...>

   >>> data['someitem'] = 'test'
   >>> print(data['someitem'])
   test

   >>> data = zsession['some.other.package']
   >>> data['info'] = 'Grok !'
