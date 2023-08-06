from .interfaces import ISession, ISessionConfig
from .utilities import ImmutableDict

import zope.component
from beaker.session import SessionObject
from zope.interface import Interface
from zope.schema import URI, Bool, ASCIILine, TextLine, Int
from zope.publisher.interfaces.http import IHTTPRequest


class ISessionDirective(Interface):
    """
    The name of the view that should be the default.

    This name refers to view that should be the
    view used by default (if no view name is supplied
    explicitly).
    """
    secret = TextLine(
        title=u"Secret passphrase",
        description=(
            u"Used with the HMAC to ensure session integrity. " +
            u"This value should ideally be a randomly generated string."),
        required=True,
        )

    validate_key = TextLine(
        title=u"Validation key",
        required=True,
        )

    environ_key = TextLine(
        title=u"WSGI environ key",
        required=False,
        default=u"beaker.session",
        )

    data_dir = URI(
        title=u"Data directory",
        required=False,
        )

    invalidate_corrupt = Bool(
        title=u"Invalidated corrupt session",
        required=False,
        default=True,
        )

    secure = Bool(
        title=u"Secure cookie",
        description=(
            u"Whether or not the session cookie should be marked as secure." +
            u" When marked as secure, browsers are instructed to not send " +
            u"the cookie over anything other than an SSL connection."),
        required=False,
        default=True,
        )

    name = TextLine(
        title=u"Registration name",
        required=False,
        default=u'',
        )
    
    key = ASCIILine(
        title=u"ID Key",
        required=False,
        description=u"Name of the cookie key used to save the session under.",
        default='beaker.session.id',
        )

    log_file = URI(
        title=u"Log file",
        required=False,
        )
    
    timeout = Int(
        title=u"Time to live",
        required=False,
        default=600,
        )

    type = ASCIILine(
        title=u"Session type",
        required=False,
        default="cookie",
        )


def beakerSession(_context, secret, validate_key, environ_key="beaker.session",
                data_dir="", invalidate_corrupt=True, secure=True,
                key='beaker.session.id', log_file='', timeout=600,
                type='cookie', name=u''):

    config = ImmutableDict(
        data_dir=data_dir,
        invalidate_corrupt=invalidate_corrupt,
        key=key,
        log_file=log_file,
        secret=secret,
        timeout=timeout,
        type=type,
        validate_key=validate_key)

    def beaker_session(request):
        session = request._environ.get(environ_key, None)
        if session is not None:
            return session

        session = SessionObject(request, **config)
        request._environ[environ_key] = session
        return session

    _context.action(
        discriminator=('utility', ISessionConfig, name),
        callable=zope.component.provideUtility,
        args=(config, ISessionConfig, name),
    )

    adapts = (IHTTPRequest,)

    _context.action(
        discriminator=('adapter', adapts, ISession, name),
        callable=zope.component.provideAdapter,
        args=(beaker_session, adapts, ISession, name),
    )
