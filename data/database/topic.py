from typing import List


class Topic:
    """
    Database component that stores a single topic.
    """

    def __init__(
        self,
        name: str,
        parents: List[str] = [],
        children: List[str] = [],
        paperNames: List[str] = [],
        authorNames: List[str] = [],
    ):

        self.name = name
        self.parents = parents
        self.children = children
        self.paperNames = paperNames
        self.authorNames = authorNames
