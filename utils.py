from config import KEYS

def printQueryResult(result):

    # Iterate over results
    for row in result:
        
        # Print value of each key individually
        print('------------------------\n')
        for key, value in zip(KEYS['papers'], row):
            print("%s: %s" % (key, str(value)))
        print("")
            
def createTable(name, keys):
    """
    Returns a string containing an SQL command to create a table with ``name``
    containing columns with names/datatypes given in ``keys``.
    """

    command = "CREATE TABLE %s (" % name
    for i, (key, key_type) in enumerate(keys.items()):
        command += "%s %s" % (key, key_type)
        if i < len(keys) - 1:
            command += ", "
    command += ")"

    return command
