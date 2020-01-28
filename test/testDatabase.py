import unittest
import copy
import datetime

from data.database.database import Database
from data.database.paper import Paper
from data.database.topic import Topic
from data.database.author import Author
from scraping import getBibInfo

PAPERS = {
    "fill": [
        {
            "name": "The Measure of Intelligence",
            "link": "https://arxiv.org/abs/1911.01547",
            "topics": {"artificial intelligence", "philosophy"},
            "parents": set(),
            "children": set(),
        },
        {
            "name": "Generalization Bounds for Convolutional Neural Networks",
            "link": "https://arxiv.org/abs/1910.01487",
            "topics": {"theoretical deep learning", "deep computer vision"},
            "parents": {"The Measure of Intelligence"},
            "children": set(),
        },
        {
            "name": "Deep Learning for Limit Order Books",
            "link": "https://arxiv.org/abs/1601.01987",
            "topics": {"deep learning", "stock trading"},
            "parents": set(),
            "children": {"The Measure of Intelligence"},
        },
        {
            "name": "Learning to Reinforcement Learn",
            "link": "https://arxiv.org/abs/1611.05763",
            "topics": {"deep reinforcement learning", "meta learning"},
            "parents": {"Deep Learning for Limit Order Books"},
            "children": {"Generalization Bounds for Convolutional Neural Networks"},
        },
        {
            "name": "Sim-to-Real Transfer of Robotic Control with Dynamics Randomization",
            "link": "https://arxiv.org/abs/1710.06537",
            "topics": {"deep reinforcement learning", "robotics"},
            "parents": {"Generalization Bounds for Convolutional Neural Networks"},
            "children": set(),
        },
    ],
    "new": [
        {
            "name": "Emergent Coordination through Competition",
            "link": "https://arxiv.org/abs/1902.07151",
            "topics": {
                "deep multi agent reinforcement learning",
                "emergent intelligence",
            },
            "parents": {"Learning to Reinforcement Learn"},
            "children": set(),
        }
    ],
}


class TestDatabase(unittest.TestCase):
    def getFilledDatabase(self):
        """
        Returns a filled database.
        """

        # Create database
        database = Database()

        # Fill with topics
        database.addTopic(Topic("computer science"))
        database.addTopic(Topic("mathematics"))
        database.addTopic(Topic("philosophy"))
        database.addTopic(
            Topic("artificial intelligence", parents={"computer science"})
        )
        database.addTopic(Topic("deep learning", parents={"artificial intelligence"}))
        database.addTopic(Topic("computer vision", parents={"artificial intelligence"}))
        database.addTopic(
            Topic("deep computer vision", parents={"deep learning", "computer vision"})
        )
        database.addTopic(
            Topic("reinforcement learning", parents={"artificial intelligence"})
        )
        database.addTopic(
            Topic(
                "deep reinforcement learning",
                parents={"deep learning", "reinforcement learning"},
            )
        )
        database.addTopic(
            Topic("theoretical deep learning", parents={"deep learning", "mathematics"})
        )
        database.addTopic(Topic("stock trading", parents={"mathematics"}))
        database.addTopic(Topic("robotics", parents={"computer science"}))
        database.addTopic(Topic("meta learning", parents={"artificial intelligence"}))

        # Fill with papers
        for paper in PAPERS["fill"]:
            paperArgs = getBibInfo(paper["link"])
            paperArgs["topicNames"] = set(paper["topics"])
            paperArgs["parents"] = set(paper["parents"])
            paperArgs["children"] = set(paper["children"])
            paperArgs["dateAdded"] = datetime.datetime.now().strftime("%m/%d/%Y")
            paperArgs["dateRead"] = ""
            paperArgs["link"] = paper["link"]
            paperArgs["notes"] = ""

            database.addPaper(Paper(**paperArgs))

        return database

    """
    Database.addPaper
    """

    def testAddPaper_1(self):
        """ Add a paper to an empty database. """

        database = Database()
        paperArgs = getBibInfo(PAPERS["new"][0]["link"])
        topics = ["testTopic"]
        paperArgs["topicNames"] = set(topics)
        paper = Paper(**paperArgs)
        database.addPaper(paper)

        expectedPapers = {paper.name: paper}
        expectedTopics = {
            topicName: Topic(
                topicName, paperNames={paper.name}, authorNames=paper.authorNames
            )
            for topicName in paper.topicNames
        }
        expectedAuthors = {
            authorName: Author(
                authorName, paperNames={paper.name}, topicNames=paper.topicNames
            )
            for authorName in paper.authorNames
        }

        self.assertEqual(database.papers, expectedPapers)
        self.assertEqual(database.topics, expectedTopics)
        self.assertEqual(database.authors, expectedAuthors)

    def testAddPaper_2(self):
        """ Add a paper to database, with parent and child. """

        database = self.getFilledDatabase()
        paperArgs = getBibInfo(PAPERS["new"][0]["link"])
        topics = ["testTopic"]
        paperArgs["topicNames"] = set(topics)
        paper = Paper(**paperArgs)

        # Copy database state before adding new paper to it
        expectedPapers = dict(database.papers)
        expectedTopics = dict(database.topics)
        expectedAuthors = dict(database.authors)
        database.addPaper(paper)

        # Construct expected papers, topics, and authors
        expectedPapers[paper.name] = paper
        for topicName in topics:
            if topicName in expectedTopics:
                expectedTopics[topicName].paperNames.add(paper.name)
                for authorName in paper.authorNames:
                    expectedTopics[topicName].authorNames.add(authorName)
            else:
                expectedTopics[topicName] = Topic(
                    topicName, paperNames={paper.name}, authorNames=paper.authorNames
                )
        for authorName in paper.authorNames:
            if authorName in expectedAuthors:
                expectedAuthors[authorName].paperNames.add(paper.name)
                for topicName in topics:
                    expectedAuthors[authorName].topicNames.add(topicName)
            else:
                expectedAuthors[authorName] = Author(
                    authorName, paperNames={paper.name}, topicNames=paper.topicNames
                )

        self.assertEqual(database.papers, expectedPapers)
        self.assertEqual(database.topics, expectedTopics)
        self.assertEqual(database.authors, expectedAuthors)

    """
    Tests Database.addTopic
    """

    def testAddTopic_1(self):
        """ Add a topic to a database with a single paper. """

        database = Database()
        paperArgs = getBibInfo(PAPERS["new"][0]["link"])
        paper = Paper(**paperArgs)
        database.addPaper(paper)
        topic = Topic("testTopic", paperNames={paper.name})
        database.addTopic(topic)

        # Modify paper and topic
        expectedPaper = copy.deepcopy(paper)
        expectedPaper.topicNames.add(topic.name)
        expectedTopic = copy.deepcopy(topic)
        expectedTopic.authorNames |= expectedPaper.authorNames

        expectedPapers = {expectedPaper.name: expectedPaper}
        expectedTopics = {expectedTopic.name: expectedTopic}
        expectedAuthors = {
            authorName: Author(
                authorName, paperNames={paper.name}, topicNames=paper.topicNames
            )
            for authorName in paper.authorNames
        }

        self.assertEqual(database.papers, expectedPapers)
        self.assertEqual(database.topics, expectedTopics)
        self.assertEqual(database.authors, expectedAuthors)

    def testAddTopic_2(self):
        """
        Add a topic to database, with parent and child topic, and linked to an
        existing paper.
        """

        # Add topic to database
        database = self.getFilledDatabase()
        linkedPaperName = list(database.papers.keys())[0]
        parents = {"mathematics"}
        children = {"stock trading"}
        topicName = "finance"
        topic = Topic(topicName, paperNames={linkedPaperName}, parents=parents,
                children=children)
        expectedPapers = dict(database.papers)
        expectedTopics = dict(database.topics)
        expectedAuthors = dict(database.authors)
        database.addTopic(topic)

        # Build expected output
        expectedPapers[linkedPaperName].topicNames.add(topicName)
        expectedTopics[topicName] = topic
        for parent in parents:
            expectedTopics[parent].children.add(topicName)
        for child in children:
            expectedTopics[child].parents.add(topicName)
        for authorName in database.papers[linkedPaperName].authorNames:
            expectedAuthors[authorName].topicNames.add(topicName)

        self.assertEqual(database.papers, expectedPapers)
        self.assertEqual(database.topics, expectedTopics)
        self.assertEqual(database.authors, expectedAuthors)

    """
    Tests Database.removePaper
    """

    def testRemovePaper_1(self):
        """ Remove isolated paper from database. """

        # Create database
        database = Database()
        paperArgs = getBibInfo(PAPERS["new"][0]["link"])
        topics = ["testTopic"]
        paperArgs["topicNames"] = set(topics)
        paper = Paper(**paperArgs)
        database.addPaper(paper)

        # Remove paper
        database.removePaper(paper.name)

        # Check results
        expectedPapers = {}
        expectedTopics = {topicName: Topic(topicName) for topicName in topics}
        expectedAuthors = {
            authorName: Author(authorName) for authorName in paper.authorNames
        }

        self.assertEqual(database.papers, expectedPapers)
        self.assertEqual(database.topics, expectedTopics)
        self.assertEqual(database.authors, expectedAuthors)

    def testRemovePaper_2(self):
        """ Remove paper with parent, child, and topics from database. """

        # Get filled database
        database = self.getFilledDatabase()
        paperName = "Generalization Bounds for Convolutional Neural Networks"
        expectedPapers = dict(database.papers)
        expectedTopics = dict(database.topics)
        expectedAuthors = dict(database.authors)
        database.removePaper(paperName)

        # Build expected output
        parents = expectedPapers[paperName].parents
        children = expectedPapers[paperName].children
        topicNames = expectedPapers[paperName].topicNames
        authorNames = expectedPapers[paperName].authorNames
        del expectedPapers[paperName]
        print(parents)
        print(children)
        print(expectedPapers.keys())
        for parent in parents:
            expectedPapers[parent].children.remove(paperName)
        for child in children:
            expectedPapers[child].parents.remove(paperName)
        for parent in parents:
            for child in children:
                expectedPapers[parent].children.add(child)
                expectedPapers[child].parents.add(parent)
        for topicName in topicNames:
            expectedTopics[topicName].papers.remove(paperName)
        for authorName in authorNames:
            expectedTopics[authorName].papers.remove(paperName)
        for topicName in topicNames:
            expectedTopics[topicName].authorNames = {}
            for paper in expectedTopics[topicName].paperNames:
                expectedTopics[topicName].authorNames |= expectedPapers[paper].authorNames
        for authorName in authorNames:
            expectedAuthors[authorName].topicNames = {}
            for paper in expectedAuthors[authorName].paperNames:
                expectedAuthors[authorName].topicNames |= expectedPapers[paper].topicNames

        self.assertEqual(database.papers, expectedPapers)
        self.assertEqual(database.topics, expectedTopics)
        self.assertEqual(database.authors, expectedAuthors)

    """
    Tests Database.removeTopic
    """

    def testRemoveTopic_1(self):
        """ Remove isolated topic from database. """

        output = 1
        expected = 2
        self.assertEqual(output, expected)

    def testRemoveTopic_2(self):
        """ Remove topic with parent, child, and papers from database. """

        output = 1
        expected = 2
        self.assertEqual(output, expected)

    """
    Tests Database.getSubtopics
    """

    def testGetSubtopics_1(self):
        """ Get subtopics from isolated topic. """

        output = 1
        expected = 2
        self.assertEqual(output, expected)

    def testGetSubtopics_2(self):
        """ Get subtopics from topic with children. """

        output = 1
        expected = 2
        self.assertEqual(output, expected)

    """
    Tests Database.getPapersFromTopics
    """

    def testGetPapersFromTopics_1(self):
        """ Get papers from isolated topic. """

        output = 1
        expected = 2
        self.assertEqual(output, expected)

    def testGetPapersFromTopics_2(self):
        """ Get papers from topic with children. """

        output = 1
        expected = 2
        self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main()
