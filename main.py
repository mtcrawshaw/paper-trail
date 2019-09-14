from utils import load_papers, save_papers
from config import KEYS

def print_action_prompt():

    msg = "Enter the number corresponding to an action!\n"
    msg += "(1) Print list of papers with information.\n"
    msg += "(2) Add a paper to the list.\n"
    msg += "(3) Remove a paper from the list.\n"
    msg += "(4) Revert back to original list of papers.\n"
    msg += "(Anything else) Quit program.\n\n"
    msg += "Action: "
    print(msg, end="")


def main():
    """ Main function to run Paper Trail program. """

    papers = load_papers()
    originalPapers = list(papers)

    while True:

        print_action_prompt()
        action = input()

        if action == '1':

            # Print papers
            for paper in papers:
                for i, (key, value) in enumerate(paper.items()):
                    print("%s: %s" % (key, str(value)))
                print("")

        elif action == '2':

            # Collect paper information
            print("Enter paper information!")
            paper = {}
            for key in KEYS:
                print("%s: ", end="")
                paper[key] = input()

            # Add paper to database
            papers.append(paper)
            print("Added paper!")

        elif action == '3':

            # Get name of paper to delete
            print("Name of paper: ", end="")
            paperName = input()
            targetPaper = None

            # Search for target paper
            for i, paper in enumerate(papers):
                if paperName == paper['name']:
                    # delete from papers
                    targetPaper = i
                    break

            # Remove paper
            if foundPaper is None:
                print("Paper name not in database!")
            else:
                papers.pop(i)
                print("Paper '%s' removed!" % paperName)

        elif action == '4':

            # Revert back to original paper list
            print("Reverting back to original list!")
            papers = list(originalPapers)

        else:
            print("Goodbye!\n")
            break

    save_papers(papers)
    

if __name__ == "__main__":
    main()
