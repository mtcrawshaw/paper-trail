from typing import Dict

from data.database.paper import Paper
from data.database.author import Author
from data.database.topic import Topic


class Database:
    """
    Database object which stores all paper information.
    """

    def __init__(self):
        """
        Init function for Database class. Must start empty.
        """

        self.papers: Dict[str, Paper] = {}
        self.authors: Dict[str, Author] = {}
        self.topics: Dict[str, Topic] = {}

    def addPaper(self, paper: Paper):
        """
        Add a paper to the database.
        """

        # Check to see if paper with same name already exists in database.
        if paper.name in self.papers:
            raise ValueError("Paper with name '%s' already in database." % paper.name)

        # Check to see if parents or children don't exist in database.
        for parentName in paper.parents:
            if parentName not in self.papers:
                raise ValueError(
                    "Paper '%s' lists paper '%s' as parent, but"
                    " paper '%s' is not in database."
                )
        for childName in paper.children:
            if childName not in self.papers:
                raise ValueError(
                    "Paper '%s' lists paper '%s' as child, but"
                    " paper '%s' is not in database."
                )

        # If the paper passes above checks, add it to database.
        self.papers[paper.name] = paper

        # Add paper to list of children for each parent, and vice versa.
        for parentName in paper.parents:
            self.papers[parentName].children += [paper.name]
        for childName in paper.children:
            self.papers[childName].parents += [paper.name]

        # Add authors and topics to database, if they don't already exist.
        # If they do exist, add paper and topics/authors.
        for authorName in paper.authorNames:
            if authorName not in self.authors:
                self.authors[authorName] = Author(
                    authorName, paperNames=[paper.name], topicNames=paper.topicNames
                )
            else:
                self.authors[authorName].paperNames += [paper.name]
                self.authors[authorName].topicNames += paper.topicNames
        for topicName in paper.topicNames:
            if topicName not in self.topics:
                self.topics[topicName] = Topic(
                    topicName, paperNames=[paper.name], authorNames=paper.authorNames
                )
            else:
                self.topics[topicName].paperNames += [paper.name]
                self.topics[topicName].authorNames += paper.authorNames

    def addTopic(self, topic: Topic):
        """
        Add a topic to the database.
        """

        # Check to see if topic with same name already exists in database.
        if topic.name in self.topics:
            raise ValueError("Topic with name '%s' already in database." % topic.name)

        # Check to see if topic is given with any papers. If so, we can't add
        # it, since we can't add papers without information about their
        # authors.
        if len(topic.paperNames) > 0:
            raise ValueError(
                "Can't add topic '%s' because it has papers "
                "already associated with it."
            )

        # If the topic passes above checks, add it to database.
        self.topics[topic.name] = topic

        # Add children and parent topics to database, if they don't already exist.
        for childName in topic.children:
            if childName not in self.topics:
                self.topics[childName] = Topic(childName, parents=[topic.name])
        for parentName in topic.parents:
            if parentName not in self.topics:
                self.topics[parentName] = Topic(parentName, children=[topic.name])

        # Add authors and papers to database, if they don't already exist.
        # If they do exist, add topic and papers/authors.
        for authorName in topic.authorNames:
            if authorName not in self.authors:
                self.authors[authorName] = Author(
                    authorName, paperNames=[], topicNames=[topic.name]
                )
            else:
                self.authors[authorName].topic += [topic.name]
                # Don't need to add to self.authors[authorName].papers, since
                # the topic must be given without any papers.
