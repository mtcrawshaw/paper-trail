import os
import sqlite3
import datetime

from scraping import getBibInfo
from utils import createTable, printQueryResult
from config import DB_PATH, KEYS

def print_action_prompt():

    msg = "Enter the number corresponding to an action!\n"
    msg += "(1) Print list of all papers.\n"
    msg += "(2) Print list of papers resulting from a given query.\n"
    msg += "(3) Add a paper to the list.\n"
    msg += "(4) Remove a paper from the list.\n"
    msg += "(Anything else) Quit program.\n\n"
    msg += "Action: "
    print(msg, end="")

def main():
    """ Main function to run Paper Trail program. """

    # Connect to database
    papersDir = os.path.dirname(DB_PATH)
    if not os.path.isdir(papersDir):
        os.makedirs(papersDir)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create tables if they don't already exist
    try:
        for tableName, tableKeys in KEYS.items():
            command = createTable(tableName, tableKeys)
            c.execute(command)
    except:
        pass

    # Action loop
    while True:

        print_action_prompt()
        action = input()
        print("")

        if action == '1':

            # Create SQL query, execute, and print
            query = "SELECT * FROM papers"
            printQueryResult(c.execute(query))

        elif action == '2':

            # Get SQL query
            print("Query: ", end="")
            query = input()

            # Try to execute query, catch invalid queries
            try:
                result = c.execute(query)
            except:
                print('Invalid query given!')
                continue

            printQueryResult(result)

        elif action == '3':

            # Collect paper information from link
            print("Enter link to paper: ", end="")
            link = input()
            paper = getBibInfo(link)

            # Check for error opening paper
            if 'err' in paper:
                print("%s\n" % paper['err'])
                continue

            # Get labels from user
            print("Enter labels separated by commas: ", end="")
            paper['labels'] = [label.strip() for label in input().split(",")]

            # Get parent from user
            print("Enter name of parent paper. "\
                  "If parent not in list, enter 'None': ", end="")
            parent = input()
            query = "SELECT title FROM papers"
            titles = [row[0] for row in c.execute(query)]
            while parent != 'None' and parent not in titles:
                print("Unrecognized parent name! Try again:")
                parent = input()
            paper['parent'] = parent

            # Add misc info
            paper['date_added'] = datetime.datetime.now().strftime("%m/%d/%Y")
            paper['date_read'] = None
            paper['link'] = link
            paper['read'] = False
            paper['recorded'] = False
            paper['notes'] = None

            # Create SQL command
            command = "INSERT INTO papers VALUES ("
            for i, key in enumerate(KEYS['papers']):
                value = paper[key]
                command += '"%s"' % value
                if i < len(KEYS['papers']) - 1:
                    command += ","
            command += ")"

            # Execute command
            c.execute(command)
            print("Paper added!\n")

        elif action == '4':

            # Get name of paper to delete
            print("Name of paper: ", end="")
            paperName = input()

            # Create and execute SQL command
            command = "DELETE FROM papers WHERE title = '%s'" % paperName
            c.execute(command)
            print("Paper '%s' removed!\n" % paperName)

        else:
            print("Goodbye!\n")
            break

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
