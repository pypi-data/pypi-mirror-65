##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

from .event import Event
from .publication import Publication
from .session import Session


class Schema(object):
    """
    user database schema for ZLMDB.
    """
    def __init__(self, db):
        self.db = db

    events: Event
    """
    CFC persisted events.
    """

    publications: Publication
    """
    CFC persistent publications.
    """

    sessions: Session
    """
    CFC persisted sessions.
    """

    @staticmethod
    def attach(db):
        """
        Factory to create a schema from attaching to a database. The schema tables
        will be automatically mapped as persistent maps and attached to the
        database slots.

        :param db: zlmdb.Database
        :return: object of Schema
        """
        schema = Schema(db)

        schema.events = db.attach_table(Event)

        schema.publications = db.attach_table(Publication)

        schema.sessions = db.attach_table(Session)

        return schema
