import sys
import requests
import logging

from collections.abc import Sequence
from koala_publisher.exceptions import exceptions


class GraphObjectPublisher:

    def __init__(self, url: str, chunk_size: int = 5000):
        self._storage_url = url
        self._chunk_size = chunk_size
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.StreamHandler(sys.stdout))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def publish(self, nodes: Sequence, edges: Sequence):
        """ Publish the graph nodes

        :param nodes: Sequence of mapping objects representing the graph nodes to be published
        :param edges: Sequence of mapping objects representing the graph edges to be published
        :return: None
        """
        self._logger.info(f"Publishing {len(nodes)} graph nodes and {len(edges)} graph edges")
        self._publish_nodes(nodes)
        self._publish_edges(edges)

    def _publish_nodes(self, graph_nodes):
        for graph_node_chunk in self._divide_into_chunks(graph_nodes):
            try:
                res = requests.put(f"{self._storage_url}/nodes", json=graph_node_chunk)
                res.raise_for_status()
            except requests.exceptions.HTTPError as err:
                self._logger.error(f"Error publishing {len(graph_node_chunk)} graph nodes to {self._storage_url}")
                raise exceptions.PublishError(err)
            else:
                self._logger.info(f"Successfully published {len(graph_node_chunk)} graph nodes")

    def _publish_edges(self, graph_edges):
        for graph_edge_chunk in self._divide_into_chunks(graph_edges):
            try:
                res = requests.put(f"{self._storage_url}/edges", json=graph_edge_chunk)
                res.raise_for_status()
            except requests.exceptions.HTTPError as err:
                self._logger.error(f"Error publishing {len(graph_edge_chunk)} graph edges to {self._storage_url}")
                raise exceptions.PublishError(err)
            else:
                self._logger.info(f"Successfully published {len(graph_edge_chunk)} graph edges")

    def _divide_into_chunks(self, graph_objects) -> Sequence:
        return [graph_objects[i:i + self._chunk_size] for i in range(0, len(graph_objects), self._chunk_size)]
