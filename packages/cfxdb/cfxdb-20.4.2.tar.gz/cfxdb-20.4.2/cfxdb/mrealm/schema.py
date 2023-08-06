##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

from .management_realm import ManagementRealm
from .node import Node
from .web_cluster import WebCluster
from .web_cluster_node_membership import WebClusterNodeMembership
from .web_service import WebService
from .web_service_json import WebServiceJson
from .web_service_node_info import WebServiceNodeInfo
from .web_service_static import WebServiceStatic


class Schema(object):
    """
    user database schema for ZLMDB.
    """
    def __init__(self, db):
        self.db = db

    management_realms: ManagementRealm
    """
    CFC management realms.
    """

    nodes: Node
    """
    CFC nodes.
    """

    web_cluster: WebCluster
    """
    CFC web clusters.
    """

    web_cluster_node_memberships: WebClusterNodeMembership
    """
    CFC web clusters node memberships.
    """

    web_services: WebService
    """
    CFC web services.
    """

    web_services_json: WebServiceJson
    """
    CFC web services of type json
    """

    web_services_node_info: WebServiceNodeInfo
    """
    CFC web services of type nodeinfo
    """

    web_services_static: WebServiceStatic
    """
    CFC static web services.
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

        schema.management_realms = db.attach_table(ManagementRealm)

        schema.nodes = db.attach_table(Node)

        schema.web_cluster = db.attach_table(WebCluster)

        schema.web_cluster_node_memberships = db.attach_table(WebClusterNodeMembership)

        schema.web_services = db.attach_table(WebService)

        schema.web_services_json = db.attach_table(WebServiceJson)

        schema.web_services_node_info = db.attach_table(WebServiceNodeInfo)

        schema.web_services_static = db.attach_table(WebServiceStatic)

        return schema
