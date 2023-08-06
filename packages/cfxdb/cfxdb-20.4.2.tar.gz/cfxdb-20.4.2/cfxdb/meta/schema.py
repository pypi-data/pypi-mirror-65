##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

from .attribute import Attributes


class Schema(object):
    """
    Generic metadata, like documentation, tags, comments and reactions that
    can be attach on any object with an UUID.
    """

    attributes: Attributes
    """
    Generic **meta data attributes** for objects in other tables.
    Primary key of this table is ``(table_oid, object_oid, attribute)``.
    """
    def __init__(self, db):
        self.db = db

    @staticmethod
    def attach(db):
        """
        Attach database schema to database instance.

        :param db: Database to attach schema to.
        :type db: :class:`zlmdb.Database`
        """
        schema = Schema(db)
        schema.attributes = db.attach_table(Attributes)
        return schema
