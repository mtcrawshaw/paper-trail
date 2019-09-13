import os
import pickle

from config import PAPERS_PATH

def load_papers():
    """ Loads a list of papers from pickle object at PAPERS_PATH. """

    if os.path.isfile(PAPERS_PATH):
        with open(PAPERS_PATH, 'rb') as f:
            papers = pickle.load(f)
    else:
        papers = {}

    return papers

def save_papers(papers):
    """ Saves a list of papers to a pickle object at PAPERS_PATH. """

    # Create directory for papers if it doesn't yet exist.
    papersDir = os.path.dirname(PAPERS_PATH)
    if not os.path.isdir(papersDir):
        os.makedirs(papersDir)

    with open(PAPERS_PATH, 'wb') as f:
        pickle.dump(papers, f)
