from zope.interface.common.mapping import IMapping
from zope.interface import Interface
from zope import schema


class ISession(IMapping):
    """Adapt the request to ISession to obtain a Beaker session. This
    interface describes the basic Beaker session type.
    """
    id = schema.ASCIILine(title=u"SHA-1 key for the session")
    last_accessed = schema.Datetime(title=u"Last access time")

    def accessed():
        """Determine if the session has been accessed (and so needs to be
        saved).
        """

    def save():
        """Save the session (at the end of the request). This is superfluous
        if, as is the default, the ``auto`` session configuration parameter
        is set to ``True``.
        """

    def delete():
        """Mark the session for deletion.
        """

    def invalidate():
        """Invalidate the session, giving a fresh one.
        """


class ISessionConfig(IMapping):
    """Beaker session setting, registered as a utility.
    These settings are looked up to configure a session. This allows a local
    utility to override settings if required.
    """


class ICacheManager(Interface):
    """
    """
