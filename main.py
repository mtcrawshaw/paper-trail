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
            while tableName not in ["papers", "authors", "topics"]:
                print("Invalid table name! Try again: ", end="")
                tableName = input()

            # Call utils to print table
            printTable(getattr(database, tableName), tableName)

        elif action == "2":

            # Get topic name from user.
            print("Enter topic name: ", end="")
            topicName = input()

            # Output papers from topic, if topic is in database.
            if topicName in database.topics:

                # Get and print resulting papers
                resultPapers = database.getPapersFromTopics([topicName])
                printTable(resultPapers, "papers")

            else:
                print("Topic '%s' not in database!\n" % topicName)

        elif action == "3":

            # Collect paper information from link.
            print("Enter link to paper: ", end="")
            link = input()
            paperArgs = getBibInfo(link)

            # Check for error opening paper.
            if "err" in paperArgs:
                print("%s\n" % paperArgs["err"])
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
                "Enter name of parent papers. " "If no parents, just press enter: ",
                end="",
            )
            parents = set(input().split(","))
            if len(parents) == 1 and next(iter(parents)) == "":
                parents = set()
            while not all([parent in database.papers for parent in parents]):
                print("Unrecognized parent name! Try again: ", end="")
                parents = set(input().split(","))
                if len(parents) == 1 and next(iter(parents)) == "":
                    parents = set()
            paperArgs["parents"] = parents

            # Get children from user
            print(
                "Enter name of child papers. " "If no children, just press enter: ",
                end="",
            )
            children = set(input().split(","))
            if len(children) == 1 and next(iter(children)) == "":
                children = set()
            while not all([child in database.papers for child in children]):
                print("Unrecognized child name! Try again: ", end="")
                children = set(input().split(","))
                if len(children) == 1 and next(iter(children)) == "":
                    children = set()
            paperArgs["children"] = children

            # Add misc info
            paperArgs["dateAdded"] = datetime.datetime.now().strftime("%m/%d/%Y")
            paperArgs["dateRead"] = ""
            paperArgs["link"] = link
            paperArgs["read"] = False
            paperArgs["notes"] = ""

            # Create paper object and add it to database
            database.addPaper(Paper(**paperArgs))
            print("Paper '%s' added!\n" % paperArgs["name"])

        elif action == "4":

            # Get name of paper to delete
            print("Name of paper: ", end="")
            paperName = input()

            database.removePaper(paperName)
            print("Paper '%s' removed!\n" % paperName)

        elif action == "5":

            # Get name of topic, making sure that it doesn't already exist
            print("Name of topic: ", end="")
            topicName = input()
            if topicName in database.topics:
                print("Topic already in database!\n")
                continue

            # Get name of parents
            print("Name of parents, separated by commas: ", end="")
            parents = set(input().split(","))
            if len(parents) == 1 and next(iter(parents)) == "":
                parents = set()
            while not all([parent in database.topics for parent in parents]):
                print("Unrecognized parent name! Try again: ", end="")
                parents = set(input().split(","))
                if len(parents) == 1 and next(iter(parents)) == "":
                    parents = set()

            # Get name of children
            print("Name of children, separated by commas: ", end="")
            children = set(input().split(","))
            if len(children) == 1 and next(iter(children)) == "":
                children = set()
            while not all([child in database.topics for child in children]):
                print("Unrecognized child name! Try again: ", end="")
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
            database.removeTopic(topicName)
            print("Topic '%s' removed!\n" % topicName)

        else:
            print("Goodbye!\n")
            break

        # Save database
        with open(DB_PATH, "wb") as f:
            pickle.dump(database, f)


if __name__ == "__main__":
    main()
