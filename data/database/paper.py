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

    def __repr__(self):
        """
        Returns string representation of self.
        """

        return str(self.__dict__)

    def __eq__(self, other):
        """
        Returns True if self == other, otherwise returns False.
        """
        attributes = [
            "name",
            "abstract",
            "datePublished",
            "dateAdded",
            "dateRead",
            "link",
            "read",
            "parents",
            "children",
            "notes",
            "authorNames",
            "topicNames",
        ]
        return all(getattr(self, attr) == getattr(other, attr) for attr in attributes)
