from config import KEYS


def printTable(table, tableName):
    """
    Prints a table of database components (papers, authors, or topics).
    """

    for name, item in table.items():
        print("------------------------\n")
        for key in KEYS[tableName]:
            print("%s: %s" % (key, getattr(item, key)))
        print("")

    if len(table) == 0:
        print("No results!")
        print("")
