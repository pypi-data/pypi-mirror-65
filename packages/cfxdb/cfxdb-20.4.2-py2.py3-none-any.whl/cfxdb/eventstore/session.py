##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

import pprint

from cfxdb.gen.eventstore import Session as SessionGen


class Session(object):
    """
    Persisted session database object.
    """
    def __init__(self, from_fbs=None):
        self._from_fbs = from_fbs

        self._session = None
        self._joined_at = None
        self._left_at = None
        self._realm = None
        self._authid = None
        self._authrole = None

    def marshal(self):
        obj = {
            'session': self.session,
            'joined_at': self.joined_at,
            'left_at': self.left_at,
            'realm': self.realm,
            'authid': self.authid,
            'authrole': self.authrole,
        }
        return obj

    def __str__(self):
        return '\n{}\n'.format(pprint.pformat(self.marshal()))

    @property
    def session(self):
        """
        The WAMP session ID of the session.

        :returns: session ID
        :rtype: int
        """
        if self._session is None and self._from_fbs:
            self._session = self._from_fbs.Session()
        return self._session

    @session.setter
    def session(self, value):
        assert value is None or type(value) == int
        self._session = value

    @property
    def joined_at(self):
        """
        Timestamp when the session was joined by the router. Epoch time in ns.

        :returns: Epoch time in ns when session joined
        :rtype: int
        """
        if self._joined_at is None and self._from_fbs:
            self._joined_at = self._from_fbs.JoinedAt()
        return self._joined_at

    @joined_at.setter
    def joined_at(self, value):
        assert value is None or type(value) == int
        self._joined_at = value

    @property
    def left_at(self):
        """
        Timestamp when the session left the router. Epoch time in ns.

        :returns: Epoch time in ns when session left - or 0 when session currently joined
        :rtype: int
        """
        if self._left_at is None and self._from_fbs:
            self._left_at = self._from_fbs.LeftAt()
        return self._left_at

    @left_at.setter
    def left_at(self, value):
        assert value is None or type(value) == int
        self._left_at = value

    @property
    def realm(self):
        """
        The WAMP realm the session is/was joined on.

        :returns: WAMP realm
        :rtype: str
        """
        if self._realm is None and self._from_fbs:
            self._realm = self._from_fbs.Realm().decode('utf8')
        return self._realm

    @realm.setter
    def realm(self, value):
        assert value is None or type(value) == str
        self._realm = value

    @property
    def authid(self):
        """
        The WAMP authid the session was authenticated under.

        :returns: WAMP authid
        :rtype: str
        """
        if self._authid is None and self._from_fbs:
            self._authid = self._from_fbs.Authid().decode('utf8')
        return self._authid

    @authid.setter
    def authid(self, value):
        assert value is None or type(value) == str
        self._authid = value

    @property
    def authrole(self):
        """
        The WAMP authrole the session was authenticated under.

        :returns: WAMP authrole
        :rtype: str
        """
        if self._authrole is None and self._from_fbs:
            self._authrole = self._from_fbs.Authrole().decode('utf8')
        return self._authrole

    @authrole.setter
    def authrole(self, value):
        assert value is None or type(value) == str
        self._authrole = value

    @staticmethod
    def cast(buf):
        return Session(SessionGen.Session.GetRootAsSession(buf, 0))

    def build(self, builder):

        realm = self.realm
        if realm:
            realm = builder.CreateString(realm)

        authid = self.authid
        if authid:
            authid = builder.CreateString(authid)

        authrole = self.authrole
        if authrole:
            authrole = builder.CreateString(authrole)

        # now start and build a new object ..
        SessionGen.SessionStart(builder)

        SessionGen.SessionAddSession(builder, self.session)
        SessionGen.SessionAddJoinedAt(builder, self.joined_at)
        if self.left_at:
            SessionGen.SessionAddLeftAt(builder, self.left_at)
        if realm:
            SessionGen.SessionAddRealm(builder, realm)
        if authid:
            SessionGen.SessionAddAuthid(builder, authid)
        if authrole:
            SessionGen.SessionAddAuthrole(builder, authrole)

        # finish the object.
        final = SessionGen.SessionEnd(builder)

        return final
