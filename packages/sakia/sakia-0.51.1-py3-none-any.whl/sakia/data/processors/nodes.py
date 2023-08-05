import attr
import sqlite3

from duniterpy.documents.ws2p.heads import HeadV2

from sakia.constants import ROOT_SERVERS
from ..entities import Node
from duniterpy.documents import BlockUID
import logging
import time


@attr.s
class NodesProcessor:
    _repo = attr.ib()  # :type sakia.data.repositories.NodesRepo

    @classmethod
    def instanciate(cls, app):
        return cls(app.db.nodes_repo)

    def initialize_root_nodes(self, currency):
        if not self.nodes(currency):
            for pubkey in ROOT_SERVERS[currency]["nodes"]:
                node = Node(
                    currency=currency,
                    pubkey=pubkey,
                    endpoints=ROOT_SERVERS[currency]["nodes"][pubkey],
                    peer_blockstamp=BlockUID.empty(),
                    state=0,
                )
                self._repo.insert(node)

    def current_buid(self, currency):
        """
        Get current buid

        Get the latest block considered valid
        It is the most frequent last block of every known nodes

        :param str currency:
        """
        current_buid = self._repo.current_buid(currency=currency)
        return current_buid

    def synced_nodes(self, currency):
        """
        Get nodes which are in the ONLINE state.
        """
        current_buid = self._repo.current_buid(currency=currency)
        return self._repo.get_synced_nodes(currency, current_buid)

    def offline_synced_nodes(self, currency):
        """
        Get nodes which are in the ONLINE state.
        """
        current_buid = self._repo.current_buid(currency=currency)
        return self._repo.get_offline_synced_nodes(currency, current_buid)

    def synced_members_nodes(self, currency):
        """
        Get nodes which are in the ONLINE state.
        """
        current_buid = self._repo.current_buid(currency=currency)
        return self._repo.get_synced_members_nodes(currency, current_buid)

    def online_nodes(self, currency):
        """
        Get nodes which are in the ONLINE state.
        """
        return self._repo.get_online_nodes(currency)

    def delete_node(self, node):
        self._repo.drop(node)

    def update_node(self, node):
        """
        Update node in the repository.
        First involves basic checks about pubkey and primary key constraints.

        :param sakia.data.entities.Node node: the node to update
        """
        other_node = self._repo.get_one(currency=node.currency, pubkey=node.pubkey)
        if other_node:
            self._repo.update(node)
        else:
            self._repo.insert(node)
        return node

    def insert_node(self, node):
        """
        Update node in the repository.
        First involves basic checks about pubkey and primary key constraints.

        :param sakia.data.entities.Node node: the node to update
        """
        self._repo.insert(node)

    def commit_node(self, node):
        """
        Saves a node state in the db
        :param sakia.data.entities.Node node: the node updated
        """
        try:
            self._repo.insert(node)
        except sqlite3.IntegrityError:
            self._repo.update(node)

    def unknown_node(self, currency, pubkey):
        """
        Search for pubkey in the repository.

        :param str currency: Name of currency
        :param str pubkey: the pubkey to lookup
        """
        other_node = self._repo.get_one(currency=currency, pubkey=pubkey)
        return other_node is None

    def nodes(self, currency):
        """
        Get all knew nodes.
        """
        return self._repo.get_all(currency=currency)

    def root_nodes(self, currency):
        """
        Get root nodes.
        """
        return self._repo.get_all(currency=currency, root=True)

    def quality(self, currency):
        """
        Get a ratio of the synced nodes vs the rest
        """
        synced = len(self.synced_nodes(currency))
        total = len(self.nodes(currency))
        if total == 0:
            ratio_synced = 0
        else:
            ratio_synced = synced / total
        return ratio_synced

    def update_ws2p(self, currency, head):
        """
        Update the peer of a node
        :param str currency: the currency of the peer
        :param head:
        :return:
        """
        node = self._repo.get_one(pubkey=head.pubkey, currency=currency)
        if node:
            if node.current_buid < head.blockstamp:
                logging.debug("Update node: {0}".format(head.pubkey[:5]))
                node.previous_buid = node.current_buid
                node.current_buid = head.blockstamp
                # capture sofware and version
                node.software = head.software
                node.version = head.software_version

                self._repo.update(node)
                return node, True
        return node, False

    def update_peer(self, currency, peer):
        """
        Update the peer of a node
        :param str currency: the currency of the peer
        :param peer:
        :return:
        """
        node = self._repo.get_one(pubkey=peer.pubkey, currency=currency)
        if node and node.peer_blockstamp < peer.blockUID:
            logging.debug("Update node: {0}".format(peer.pubkey[:5]))
            node.endpoints = tuple(peer.endpoints)
            node.peer_blockstamp = peer.blockUID
            self._repo.update(node)
            return node, True
        return node, False

    def handle_success(self, node):
        if not node.online():
            node.last_state_change = time.time()
        node.state = max(0, node.state - 1)
        self.update_node(node)

    def handle_failure(self, node, weight=1):
        if node.state + weight > Node.FAILURE_THRESHOLD and node.online():
            node.last_state_change = time.time()
        node.state = min(5, node.state + weight)
        self.update_node(node)

    def drop_all(self, currency):
        nodes = self._repo.get_all()
        for n in nodes:
            if n.pubkey not in ROOT_SERVERS[currency].keys():
                self._repo.drop(n)
