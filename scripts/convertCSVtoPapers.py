import csv
import argparse
import pickle

def main(args):
    """ Main function for convertCSVtoPapers.py. """

    # Read in CSV file
    csvLines = []
    with open(args.csvPath, 'r') as f:
        fReader = csv.reader(f, delimiter=',')
        for row in fReader:
            csvLines.append(list(row))

    # Create papers list
    keys = ['title', 'authors', 'labels', 'date_added', 'date_read', 'link',
            'read', 'recorded', 'parent', 'notes']
    papers = []
    for i, line in enumerate(csvLines):
        if i == 0:
            continue

        paper = {}
        for element, key in zip(line, keys):

            # Parse for multi-valued elements
            if key in ['authors', 'labels']:
                element = element.split(',')
            paper[key] = element

        papers.append(dict(paper))

    # Save out papers list
    with open(args.papersPath, 'wb') as f:
        pickle.dump(papers, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('csvPath', help='Path to CSV file to convert.')
    parser.add_argument('papersPath', help='Path to pickle file to papers to.')
    args = parser.parse_args()

    main(args)
