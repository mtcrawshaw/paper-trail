import unittest
import copy

from data.database.database import Database
from data.database.paper import Paper
from data.database.topic import Topic
from data.database.author import Author
from scraping import getBibInfo

PAPER_LINKS = [
    "https://arxiv.org/abs/1906.01470",
    "https://arxiv.org/abs/1901.01753",
    "https://arxiv.org/abs/1808.04355",
    "https://arxiv.org/abs/1902.07151",
    "https://arxiv.org/abs/1810.12894",
    "https://arxiv.org/abs/1902.08438",
    "https://arxiv.org/abs/1903.08254",
    "https://arxiv.org/abs/1809.04474",
    "https://arxiv.org/abs/1511.06342",
    "https://arxiv.org/abs/1904.11455",
    "https://arxiv.org/abs/1503.02531",
]


class TestDatabase(unittest.TestCase):
    def getFilledDatabase(self):
        """
        Returns a filled database.
        """

        # Create database
        database = Database()

        # Fill with topics

        # Fill with papers

    """
    Database.addPaper
    """

    def testAddPaper_1(self):
        """ Add a paper to an empty database. """

        database = Database()
        paperArgs = getBibInfo(PAPER_LINKS[0])
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

        output = 1
        expected = 1
        self.assertEqual(output, expected)

    """
    Tests Database.addTopic
    """

    def testAddTopic_1(self):
        """ Add a topic to a database with a single paper. """

        database = Database()
        paperArgs = getBibInfo(PAPER_LINKS[0])
        paper = Paper(**paperArgs)
        database.addPaper(paper)
        topic = Topic('testTopic', paperNames={paper.name})
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
        """ Add a topic to database, with parent and child. """

        output = 1
        expected = 1
        self.assertEqual(output, expected)

    """
    Tests Database.removePaper
    """

    def testRemovePaper_1(self):
        """ Remove isolated paper from database. """

        output = 1
        expected = 1
        self.assertEqual(output, expected)

    def testRemovePaper_2(self):
        """ Remove paper with parent, child, and topics from database. """

        output = 1
        expected = 1
        self.assertEqual(output, expected)

    """
    Tests Database.removeTopic
    """

    def testRemoveTopic_1(self):
        """ Remove isolated topic from database. """

        output = 1
        expected = 1
        self.assertEqual(output, expected)

    def testRemoveTopic_2(self):
        """ Remove topic with parent, child, and papers from database. """

        output = 1
        expected = 1
        self.assertEqual(output, expected)

    """
    Tests Database.getSubtopics
    """

    def testGetSubtopics_1(self):
        """ Get subtopics from isolated topic. """

        output = 1
        expected = 1
        self.assertEqual(output, expected)

    def testGetSubtopics_2(self):
        """ Get subtopics from topic with children. """

        output = 1
        expected = 1
        self.assertEqual(output, expected)

    """
    Tests Database.getPapersFromTopics
    """

    def testGetPapersFromTopics_1(self):
        """ Get papers from isolated topic. """

        output = 1
        expected = 1
        self.assertEqual(output, expected)

    def testGetPapersFromTopics_2(self):
        """ Get papers from topic with children. """

        output = 1
        expected = 1
        self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main()
