##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

from zlmdb import table, MapTimestampUuidFlatBuffers

from cfxdb.log.mnode_log import MNodeLog


@table('256a071f-5aeb-47f3-8786-97cd8281bdb7', build=MNodeLog.build, cast=MNodeLog.cast)
class MNodeLogs(MapTimestampUuidFlatBuffers):
    """
    Persisted managed node heartbeat log records.

    Map :class:`zlmdb.MapTimestampUuidFlatBuffers` from ``(timestamp, node_id)`` to :class:`cfxdb.logs.MNodeLog`
    """
