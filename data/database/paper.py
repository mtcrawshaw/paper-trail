from typing import Set


class Paper:
    """
    Database component that stores a single paper.
    """

    def __init__(
        self,
        name: str,
        abstract: str = "",
        datePublished: str = "",
        dateAdded: str = "",
        dateRead: str = "",
        link: str = "",
        read: bool = False,
        parents: Set[str] = set(),
        children: Set[str] = set(),
        notes: str = "",
        authorNames: Set[str] = set(),
        topicNames: Set[str] = set(),
    ):

        self.name = str(name)
        self.abstract = str(abstract)
        self.datePublished = str(datePublished)
        self.dateAdded = str(dateAdded)
        self.dateRead = str(dateRead)
        self.link = str(link)
        self.read = bool(read)
        self.parents = set(parents)
        self.children = set(children)
        self.notes = str(notes)
        self.authorNames = set(authorNames)
        self.topicNames = set(topicNames)
