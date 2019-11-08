from typing import List


class Paper:
    """
    Database component that stores a single paper.
    """

    def __init__(
        self,
        name: str,
        abstract: str = [],
        datePublished: str = "",
        dateAdded: str = "",
        dateRead: str = "",
        link: str = "",
        read: bool = False,
        parents: List[str] = [],
        children: List[str] = [],
        notes: str = "",
        authorNames: List[str] = [],
        topicNames: List[str] = [],
    ):

        self.name = name
        self.abstract = abstract
        self.datePublished = datePublished
        self.dateAdded = dateAdded
        self.dateRead = dateRead
        self.link = link
        self.read = read
        self.parents = parents
        self.children = children
        self.notes = notes
        self.authorNames = authorNames
        self.topicNames = topicNames
