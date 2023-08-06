##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

from zlmdb import table, MapOidFlatBuffers, MapOidTimestampFlatBuffers

import cfxdb.eventstore.session

__all__ = (
    'Sessions',
    'Publications',
    'Events',
    'Schema',
)


@table('a674f707-69b8-4c41-b2a1-df17cec9b095',
       build=cfxdb.eventstore.session.Session.build,
       cast=cfxdb.eventstore.session.Session.cast)
class Sessions(MapOidFlatBuffers):
    """
    Persisted sessions archive.

    Map :class:`zlmdb.MapOidFlatBuffers` from ``session`` to :class:`cfxdb.eventstore.Session`
    """


@table('dd04931a-753b-4fde-8140-d66b93519c73',
       build=cfxdb.eventstore.publication.Publication.build,
       cast=cfxdb.eventstore.publication.Publication.cast)
class Publications(MapOidFlatBuffers):
    """
    Persisted publications archive.

    Map :class:`zlmdb.MapOidFlatBuffers` from ``publication`` to :class:`cfxdb.eventstore.Publication`.
    """


@table('40a9df31-6065-496f-809f-027a1879654c',
       build=cfxdb.eventstore.event.Event.build,
       cast=cfxdb.eventstore.event.Event.cast)
class Events(MapOidTimestampFlatBuffers):
    """
    Persisted events archive.


    Map :class:`zlmdb.MapOid3FlatBuffers` from ``(subscription, time_ns)`` to :class:`cfxdb.eventstore.Event`.
    """


class Schema(object):
    """
    CFC edge database schema for ZLMDB.
    """
    def __init__(self, db):
        self.db = db

    # sessions: Sessions
    sessions = None
    """
    Sessions archive.
    """

    # publications: Publications
    publications = None
    """
    Publications archive.
    """

    # events: Events
    events = None
    """
    Events archive.
    """

    @staticmethod
    def attach(db):
        """
        Factory to create a schema from attaching to a database. The schema tables
        will be automatically mapped as persistant maps and attached to the
        database slots.

        :param db: zlmdb.Database
        :return: object of Schema
        """
        schema = Schema(db)

        schema.sessions = db.attach_table(Sessions)
        schema.publications = db.attach_table(Publications)
        schema.events = db.attach_table(Events)

        return schema
