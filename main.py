import os
import sqlite3

from config import KEYS, DB_PATH

def print_action_prompt():

    msg = "Enter the number corresponding to an action!\n"
    msg += "(1) Print list of papers with information.\n"
    msg += "(2) Add a paper to the list.\n"
    msg += "(3) Remove a paper from the list.\n"
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

    # Create table
    try:
        command = "CREATE TABLE papers ("
        for i, (key, key_type) in enumerate(KEYS.items()):
            command += "%s %s" % (key, key_type)
            if i < len(KEYS) - 1:
                command += ", "
        command += ")"
        c.execute(command)
    except:
        pass

    # Action loop
    while True:

        print_action_prompt()
        action = input()
        print("")

        if action == '1':

            # Create SQL query
            query = "SELECT * FROM papers"

            # Execute and iterate over results
            for row in c.execute(query):
                
                # Print value of each key individually
                for key, value in zip(KEYS, row):
                    print("%s: %s" % (key, str(value)))
                print("")
            
        elif action == '2':

            # Collect paper information
            print("Enter paper information!")
            paper = {}
            for key in KEYS:
                print("%s: " % key, end="")
                paper[key] = input()

            # Create SQL command
            command = "INSERT INTO papers VALUES ("
            for i, (key, value) in enumerate(paper.items()):
                command += "'%s'" % value
                if i < len(paper) - 1:
                    command += ","
            command += ")"

            # Execute command
            c.execute(command)
            print("Paper added!\n")

        elif action == '3':

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
