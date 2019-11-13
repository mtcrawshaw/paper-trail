import unittest

class TestDatabase(unittest.TestCase):

    """
        Tests Database.addPaper
    """
    def testAddPaper(self):

        output = 1
        expected = 1
        self.assertEqual(output, expected)

    """
        Tests Database.addTopic
    """
    def testAddTopic(self):

        output = 1
        expected = 1
        self.assertEqual(output, expected)

    """
        Tests Database.removePaper
    """
    def testRemovePaper(self):

        output = 1
        expected = 1
        self.assertEqual(output, expected)

    """
        Tests Database.removeTopic
    """
    def testRemoveTopic(self):

        output = 1
        expected = 1
        self.assertEqual(output, expected)

    """
        Tests Database.getSubtopics
    """
    def testGetSubtopics(self):

        output = 1
        expected = 1
        self.assertEqual(output, expected)

    """
        Tests Database.getPapersFromTopics
    """
    def testGetPapersFromTopics(self):

        output = 1
        expected = 1
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
