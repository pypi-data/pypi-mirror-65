"""
K8S provides a set of services for Kubernetes.
"""

from diagrams import Node


class _K8S(Node):
    _provider = "k8s"
    _icon_dir = "resources/k8s"

    fontcolor = "#2d3436"
