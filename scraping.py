import requests

def getBibInfo(link, site='arxiv'):
    """ Get bibliographic info for a paper from a link. """

    if site not in ['arxiv']:
        raise ValueError("Site '%s' unsupported." % site)
    
    scraper = eval('%s_getBibInfo' % site)
    return scraper(link)

def arxiv_getBibInfo(link):
    """ Get bibliographic info for a paper from a link to arxiv.org. """

    # Get HTML from arxiv page
    paper = {}
    result = requests.get(link)
    lines = [line.strip() for line in result.text.split("\n")]

    # Define keywords we are looking for
    keywords = {}
    keywords[('name', 'citation_title')] = 'title'
    keywords[('name', 'citation_author')] = 'authors'
    keywords[('name', 'citation_online_date')] = 'date_published'
    keywords[('property', 'og:description')] = 'abstract'

    # Check for lines with bibliographic information
    authors = []
    for line in lines:
        if line.startswith("<meta"):

            # Parse "key=value" pairs from line
            start = line.find(" ") + 1
            end = line.find("/>")
            line = line[start:end]
            items = []
            runningItem = ""
            insideQuote = False
            for i, char in enumerate(line):
                if (char == ' ' and not insideQuote) or i == len(line) - 1:
                    key, value = runningItem.split("=")
                    value = value.strip("\"")
                    items.append((key, value))
                    runningItem = ""
                else:
                    runningItem += char
                    if char == '\"':
                        insideQuote = not insideQuote

            # Check if first key=value pair is in keywords, if so, add
            # value from second key=value pair to paper
            if items[0] in keywords:
                bibKey = keywords[items[0]]
                bibValue = items[1][1]

                # Handle multiple authors with running list
                if bibKey == 'authors':
                    authors.append(bibValue)
                else:
                    paper[bibKey] = bibValue

    paper['authors'] = list(authors)
    return paper

