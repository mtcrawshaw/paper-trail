from typing import Set


class Topic:
    """
    Database component that stores a single topic.
    """

    def __init__(
        self,
        name: str,
        parents: Set[str] = set(),
        children: Set[str] = set(),
        paperNames: Set[str] = set(),
        authorNames: Set[str] = set(),
    ):

        self.name = str(name)
        self.parents = set(parents)
        self.children = set(children)
        self.paperNames = set(paperNames)
        self.authorNames = set(authorNames)

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
            'name',
            'parents',
            'children',
            'paperNames',
            'authorNames',
        ]
        return all(getattr(self, attr) == getattr(other, attr) for attr in
                attributes)
