from urllib.request import urlopen
from bs4 import BeautifulSoup

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
    page = urlopen(link).read()
    soup = BeautifulSoup(page, "lxml")

    # Define keywords we are looking for
    keywords = {}
    keywords[('name', 'citation_title')] = 'title'
    keywords[('name', 'citation_author')] = 'authors'
    keywords[('name', 'citation_online_date')] = 'date_published'
    keywords[('property', 'og:description')] = 'abstract'

    # Find lines with bibliographic information
    authors = []
    metaTags = soup.find_all("meta")
    for metaTag in metaTags:
        for (keyWord, keyValue), bibKey in keywords.items():
            if keyWord in metaTag.attrs and metaTag[keyWord] == keyValue:
                bibValue = metaTag['content']
                bibValue = bibValue.replace('\n', ' ')

                # Handle multiple authors
                if bibKey == 'authors':
                    authors.append(bibValue)
                else:
                    paper[bibKey] = bibValue

    paper['authors'] = list(authors)
    return paper

