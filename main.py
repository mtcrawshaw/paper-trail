from utils import load_papers, save_papers

def main():
    """ Main function to run Paper Trail program. """

    papers = load_papers()
    save_papers(papers)
    

if __name__ == "__main__":
    main()
