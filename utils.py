from config import KEYS

def printQueryResult(result):

    # Iterate over results
    for row in result:
        
        # Print value of each key individually
        print('------------------------\n')
        for key, value in zip(KEYS, row):
            print("%s: %s" % (key, str(value)))
        print("")
            
