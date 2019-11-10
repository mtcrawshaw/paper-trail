from typing import Set


class Author:
    """
    Database component that stores a single author.
    """

    def __init__(
        self,
        name: str,
        paperNames: Set[str] = set(),
        topicNames: Set[str] = set(),
    ):

        self.name = name
        self.paperNames = set(paperNames)
        self.topicNames = set(topicNames)
