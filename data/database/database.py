from typing import Dict, List

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
                raise ValueError("Paper '%s' not in database." % parentName)
        for childName in paper.children:
            if childName not in self.papers:
                raise ValueError("Paper '%s' not in database." % childName)

        # If the paper passes above checks, add it to database.
        self.papers[paper.name] = paper

        # Add paper to list of children for each parent, and vice versa.
        for parentName in paper.parents:
            self.papers[parentName].children.add(paper.name)
        for childName in paper.children:
            self.papers[childName].parents.add(paper.name)

        # Add authors and topics to database, if they don't already exist.
        # If they do exist, add paper and topics/authors.
        for authorName in paper.authorNames:
            if authorName not in self.authors:
                self.authors[authorName] = Author(
                    authorName, paperNames={paper.name}, topicNames=paper.topicNames
                )
            else:
                self.authors[authorName].paperNames.add(paper.name)
                self.authors[authorName].topicNames |= paper.topicNames
        for topicName in paper.topicNames:
            if topicName not in self.topics:
                self.topics[topicName] = Topic(
                    topicName, paperNames={paper.name}, authorNames=paper.authorNames
                )
            else:
                self.topics[topicName].paperNames.add(paper.name)
                self.topics[topicName].authorNames |= paper.authorNames

    def addTopic(self, topic: Topic):
        """
        Add a topic to the database.
        """

        # Check to see if topic with same name already exists in database.
        if topic.name in self.topics:
            raise ValueError("Topic with name '%s' already in database." % topic.name)

        # Check to see if topic is given with any papers that don't already
        # exist. If so, we can't add it, since we can't add papers without
        # information about their authors.
        if any(paperName not in self.papers for paperName in topic.paperNames):
            raise ValueError(
                "Can't add topic '%s' because it has papers "
                "associated with it that aren't yet in database."
            )

        # Add children and parent topics to database, if they don't already exist.
        # If they do exist, add new topic as parent/child.
        for childName in topic.children:
            if childName not in self.topics:
                self.topics[childName] = Topic(childName, parents=[topic.name])
            else:
                self.topics[childName].parents.add(topic.name)
        for parentName in topic.parents:
            if parentName not in self.topics:
                self.topics[parentName] = Topic(parentName, children=[topic.name])
            else:
                self.topics[parentName].children.add(topic.name)

        # Add authors and papers to database, if they don't already exist.
        # If they do exist, add topic and papers/authors.
        for authorName in topic.authorNames:
            if authorName not in self.authors:
                self.authors[authorName] = Author(
                    authorName, paperNames=set(), topicNames={topic.name}
                )
            else:
                self.authors[authorName].topicNames.add(topic.name)
        for paperName in topic.paperNames:
            # Papers must already exist, by the check earlier in this method.
            self.papers[paperName].topicNames.add(topic.name)

        # For any papers under topic, add authors of those papers to topic, and
        # add topic to those authors.
        for paperName in topic.paperNames:
            for authorName in self.papers[paperName].authorNames:
                topic.authorNames.add(authorName)
                self.authors[authorName].topicNames.add(topic.name)
        
        # Add topic to database.
        self.topics[topic.name] = topic


    def removePaper(self, paperName: str):
        """
        Removes a paper from the database.
        """

        if paperName in self.papers:

            # Remove as child from parent papers, and as parent from child papers
            for childName in self.papers[paperName].children:
                self.papers[childName].parents.remove(paperName)
            for parentName in self.papers[paperName].parents:
                self.papers[parentName].children.remove(paperName)

            # Set children of paperName as children of parents of paperName, to
            # preserve ancestor-descendant relationships.
            for childName in self.papers[paperName].children:
                for parentName in self.papers[paperName].parents:
                    self.papers[childName].parents.add(parentName)
                    self.papers[parentName].children.add(childName)

            # Remove from authors and topics
            for authorName in self.papers[paperName].authorNames:
                self.authors[authorName].paperNames.remove(paperName)
            for topicName in self.papers[paperName].topicNames:
                self.topics[topicName].paperNames.remove(paperName)

            # Remove from papers
            del self.papers[paperName]

        else:
            raise ValueError("Paper '%s' not in database." % paperName)

    def removeTopic(self, topicName: str):
        """
        Removes a topic from the database.
        """

        if topicName in self.topics:

            # Remove as child from parent topics, and as parent from child topics
            for childName in self.topics[topicName].children:
                self.topics[childName].parents.remove(topicName)
            for parentName in self.topics[topicName].parents:
                self.topics[parentName].children.remove(topicName)

            # Set children of topicName as children of parents of topicName, to
            # preserve ancestor-descendant relationships.
            for childName in self.topics[topicName].children:
                for parentName in self.topics[topicName].parents:
                    self.topics[childName].parents.add(parentName)
                    self.topics[parentName].children.add(childName)

            # Set papers under removed topic under parents of removed topic.
            for paperName in self.topics[topicName].paperNames:
                for parentName in self.topics[topicName].parents:
                    self.papers[paperName].topicNames.add(parentName)
                    self.topics[parentName].paperNames.add(paperName)

            # Remove from papers and authors
            for paperName in self.topics[topicName].paperNames:
                self.papers[paperName].topicNames.remove(topicName)
            for authorName in self.topics[topicName].authorNames:
                self.authors[authorName].topicNames.remove(topicName)

            # Remove from topics
            del self.topics[topicName]

        else:
            raise ValueError("Topic '%s' not in database." % topicName)

    def getSubtopics(self, topicName: str) -> List[Topic]:
        """
        Returns all descendant topics of a given topic.
        """

        topics = []
        topicQueue = [topicName]
        while len(topicQueue) > 0:
            currentTopic = topicQueue.pop(0)
            topics.append(currentTopic)
            topicQueue += list(self.topics[currentTopic].children)

        return topics

    def getPapersFromTopics(self, topicNames: List[str]) -> List[Paper]:
        """
        Returns all papers under a list of given topics, including the papers
        under sub-topics of given topics.
        """

        paperNames = []

        # Iterate over topicNames
        for topicName in topicNames:

            if topicName not in self.topics:
                raise ValueError("Topic '%s' not in database." % topicName)

            # Get subtopics and paper names under subtopics
            subtopicNames = self.getSubtopics(topicName)
            for subtopicName in subtopicNames:
                paperNames += list(self.topics[subtopicName].paperNames)

        # Remove redundant paper names
        paperNames = list(set(paperNames))

        # Get papers from paperNames
        papers = {paperName: self.papers[paperName] for paperName in paperNames}
        return papers

    def __eq__(self, other):
        """
        Returns True if self == other, otherwise returns False.
        """

        attributes = ['papers', 'topics', 'authors']
        return all(getattr(self, attr) == getattr(other, attr) for attr in attributes)
