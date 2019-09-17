import os
import csv
import argparse
import sqlite3

# HARDCODE
KEYS = {
        'title': 'text',
        'abstract': 'text',
        'authors': 'text',
        'labels': 'text',
        'date_published': 'date',
        'date_added': 'date',
        'date_read': 'date',
        'link': 'text',
        'read': 'text',
        'recorded': 'text',
        'parent': 'text',
        'notes': 'text'
}

def main(args):
    """ Main function for convertCSVtoPapers.py. """

    # Check if given output file already exists
    if os.path.isfile(args.DBpath):
        print("Given output path '%s' already exists!" % args.DBpath)
        exit()

    # Read in CSV file
    csvLines = []
    with open(args.csvPath, 'r') as f:
        fReader = csv.reader(f, delimiter=',')
        for row in fReader:
            csvLines.append(list(row))

    # Connect to database
    papersDir = os.path.dirname(args.DBpath)
    if not os.path.isdir(papersDir):
        os.makedirs(papersDir)
    conn = sqlite3.connect(args.DBpath)
    c = conn.cursor()

    # Add table to database
    command = "CREATE TABLE papers ("
    for i, (key, key_type) in enumerate(KEYS.items()):
        command += "%s %s" % (key, key_type)
        if i < len(KEYS) - 1:
            command += ", "
    command += ")"
    c.execute(command)

    # Add rows to table
    for i, line in enumerate(csvLines):
        if i == 0:
            continue

        # Create insert command
        command = "INSERT INTO papers VALUES ("
        for i, (element, (key, key_type)) in enumerate(zip(line, KEYS.items())):
            command += "'%s'" % element.replace('\'', '\"')
            if i < len(line) - 1:
                command += ","
        command += ")"

        # Execute command
        c.execute(command)

    # Save out database
    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('csvPath', help='Path to CSV file to convert.')
    parser.add_argument('DBpath', help='Path to output DB for papers.')
    args = parser.parse_args()

    main(args)
