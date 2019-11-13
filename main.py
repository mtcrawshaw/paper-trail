import os
import pickle
import datetime
from pprint import pprint

from scraping import getBibInfo
from utils import printTable
from config import DB_PATH, KEYS
from data.database.database import Database, Paper, Topic


def print_action_prompt():

    msg = "Enter the number corresponding to an action!\n"
    msg += "(1) Print entire table.\n"
    msg += "(2) Print papers within a topic.\n"
    msg += "(3) Add a paper.\n"
    msg += "(4) Remove a paper.\n"
    msg += "(5) Add a topic.\n"
    msg += "(6) Remove a topic.\n"
    msg += "(Anything else) Quit program.\n\n"
    msg += "Action: "
    print(msg, end="")


def main():
    """ Main function to run Paper Trail program. """

    # Load database. If none exists, create one.
    papersDir = os.path.dirname(DB_PATH)
    if not os.path.isdir(papersDir):
        os.makedirs(papersDir)
    if os.path.isfile(DB_PATH):
        with open(DB_PATH, "rb") as f:
            database = pickle.load(f)
    else:
        database = Database()

    # Action loop
    while True:

        print_action_prompt()
        action = input()
        print("")

        if action == "1":

            # Get table name to print.
            print(
                "Enter table name. Should be either 'papers', 'authors', or"
                " 'topics': ",
                end="",
            )
            tableName = input()

            # Call utils to print table
            try:
                printTable(getattr(database, tableName), tableName)
            except AttributeError:
                print("Database has no table '%s'" % tableName)

        elif action == "2":

            # Get topic name from user.
            print("Enter topic name: ", end="")
            topicName = input()

            # Get and print resulting papers
            try:
                resultPapers = database.getPapersFromTopics([topicName])
                printTable(resultPapers, "papers")
            except ValueError as err:
                print("%s\n" % err)

        elif action == "3":

            # Collect paper information from link.
            print("Enter link to paper: ", end="")
            link = input()

            # Check for error opening paper.
            try:
                paperArgs = getBibInfo(link)
            except ValueError as err:
                print("Error opening link: \"%s\"\n" % err)
                continue

            # Get topics from user
            print("Enter topic names separated by commas: ", end="")
            paperArgs["topicNames"] = set(
                [label.strip() for label in input().split(",")]
            )
            if (
                len(paperArgs["topicNames"]) == 1
                and next(iter(paperArgs["topicNames"])) == ""
            ):
                paperArgs["topicNames"] = set()

            # Get parents from user
            print(
                "Enter name of parent papers, individually, and enter an empty "\
                "entry when done: ",
                end="",
            )
            parents = []
            parent = input()
            while parent != "":
                parents.append(parent)
                print("Next parent: ", end="")
                parent = input()
            paperArgs["parents"] = parents

            # Get children from user
            print(
                "Enter name of child papers, individually, and enter an empty "\
                "entry when done: ",
                end="",
            )
            children = []
            child = input()
            while child != "":
                children.append(child)
                print("Next child: ", end="")
                child = input()
            paperArgs["children"] = children

            # Add misc info
            paperArgs["dateAdded"] = datetime.datetime.now().strftime("%m/%d/%Y")
            paperArgs["dateRead"] = ""
            paperArgs["link"] = link
            paperArgs["read"] = False
            paperArgs["notes"] = ""

            # Create paper object and add it to database
            try:
                database.addPaper(Paper(**paperArgs))
                print("Paper '%s' added!\n" % paperArgs["name"])
            except (KeyError, ValueError) as err:
                print("%s\n" % err)
                continue

        elif action == "4":

            # Get name of paper to delete
            print("Name of paper: ", end="")
            paperName = input()

            try:
                database.removePaper(paperName)
                print("Paper '%s' removed!\n" % paperName)
            except ValueError as err:
                print("%s\n" % err)
                continue

        elif action == "5":

            # Get name of topic, making sure that it doesn't already exist
            print("Name of topic: ", end="")
            topicName = input()

            # Get name of parents
            print("Name of parents, separated by commas: ", end="")
            parents = set(input().split(","))
            if len(parents) == 1 and next(iter(parents)) == "":
                parents = set()

            # Get name of children
            print("Name of children, separated by commas: ", end="")
            children = set(input().split(","))
            if len(children) == 1 and next(iter(children)) == "":
                children = set()

            # Add topic to database
            database.addTopic(Topic(topicName, parents=parents, children=children))
            print("Topic '%s' added!\n" % topicName)

        elif action == "6":

            # Get name of topic
            print("Name of topic: ", end="")
            topicName = input()

            # Remove topic from database
            try:
                database.removeTopic(topicName)
                print("Topic '%s' removed!\n" % topicName)
            except ValueError as err:
                print("%s\n" % err)
                continue

        else:
            print("Goodbye!\n")
            break

        # Save database
        with open(DB_PATH, "wb") as f:
            pickle.dump(database, f)


if __name__ == "__main__":
    main()
