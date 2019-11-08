from typing import List


class Author:
    """
    Database component that stores a single author.
    """

    def __init__(
        self,
        name: str,
        paperNames: List[str] = [],
        topicNames: List[str] = [],
    ):

        self.name = name
        self.paperNames = paperNames
        self.topicNames = topicNames
