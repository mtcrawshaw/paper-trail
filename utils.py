from config import KEYS

def printTable(database, tableName):

    for name, item in getattr(database, tableName).items():
        print('------------------------\n')
        for key in KEYS[tableName]:
            print("%s: %s" % (key, getattr(item, key)))
        print("")
