import os
import pickle
import datetime

from scraping import getBibInfo
from utils import printTable
from config import DB_PATH, KEYS
from data.database.database import Database, Paper


def print_action_prompt():

    msg = "Enter the number corresponding to an action!\n"
    msg += "(1) Print entire table.\n"
    msg += "(2) Add a paper to the list.\n"
    msg += "(3) Remove a paper from the list.\n"
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
            printTable(database, tableName)

        elif action == "2":

            # Collect paper information from link.
            print("Enter link to paper: ", end="")
            link = input()
            paperArgs = getBibInfo(link)

            # Check for error opening paper.
            if "err" in paperArgs:
                print("%s\n" % paperArgs["err"])
                continue

            # Get labels from user
            print("Enter topic names separated by commas: ", end="")
            paperArgs["topicNames"] = [label.strip() for label in input().split(",")]

            # Get parents from user
            print(
                "Enter name of parent papers. " "If no parents, just press enter: ",
                end="",
            )
            parents = input().split()
            while not all([parent in database.papers for parent in parents]):
                print("Unrecognized parent name! Try again:")
                parents = input().split()
            paperArgs["parents"] = parents

            # Get children from user
            print(
                "Enter name of child papers. " "If no children, just press enter: ",
                end="",
            )
            children = input().split()
            while not all([child in database.papers for child in children]):
                print("Unrecognized child name! Try again:")
                children = input().split()
            paperArgs["children"] = children

            # Add misc info
            paperArgs["dateAdded"] = datetime.datetime.now().strftime("%m/%d/%Y")
            paperArgs["dateRead"] = ""
            paperArgs["link"] = link
            paperArgs["read"] = False
            paperArgs["notes"] = ""

            # Create paper object and add it to database
            database.addPaper(Paper(**paperArgs))
            print("Paper added!\n")

        elif action == "3":

            # Get name of paper to delete
            print("Name of paper: ", end="")
            paperName = input()

            # Create and execute SQL command
            if paperName in database.papers:
                del database.papers[paperName]
                print("Paper '%s' removed!\n" % paperName)
            else:
                print("Paper '%s' not in database!\n" % paperName)

        else:
            print("Goodbye!\n")
            break

        # Save database
        with open(DB_PATH, "wb") as f:
            pickle.dump(database, f)


if __name__ == "__main__":
    main()
