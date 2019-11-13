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
            'paperNames',
            'topicNames',
        ]
        return all(getattr(self, attr) == getattr(other, attr) for attr in
                attributes)
