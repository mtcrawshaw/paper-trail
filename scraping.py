from urllib.request import urlopen
from bs4 import BeautifulSoup


def getBibInfo(link, site="arxiv"):
    """ Get bibliographic info for a paper from a link. """

    if site not in ["arxiv"]:
        raise ValueError("Site '%s' unsupported." % site)

    scraper = eval("%s_getBibInfo" % site)
    return scraper(link)


def arxiv_getBibInfo(link):
    """ Get bibliographic info for a paper from a link to arxiv.org. """

    # Get HTML from arxiv page
    paperArgs = {}
    try:
        page = urlopen(link).read()
    except:
        return {"err": "Invalid link!"}
    soup = BeautifulSoup(page, "lxml")

    # Define keywords we are looking for
    keywords = {}
    keywords[("name", "citation_title")] = "name"
    keywords[("name", "citation_author")] = "authorNames"
    keywords[("name", "citation_online_date")] = "datePublished"
    keywords[("property", "og:description")] = "abstract"

    # Find lines with bibliographic information
    paperArgs["authorNames"] = []
    metaTags = soup.find_all("meta")
    for metaTag in metaTags:
        for (keyWord, keyValue), bibKey in keywords.items():
            if keyWord in metaTag.attrs and metaTag[keyWord] == keyValue:
                bibValue = metaTag["content"]
                bibValue = bibValue.replace("\n", " ")

                # Handle multiple authors
                if bibKey == "authorNames":

                    # Switch format from "last, first middle" to "first middle last"
                    author = bibValue
                    names = author.split(",")
                    author = ("%s %s" % (names[1], names[0])).strip()
                    paperArgs["authorNames"].append(author)
                else:
                    paperArgs[bibKey] = bibValue

    # Clean inputs
    reformat = lambda x: x.replace('"', "'")
    for bibKey, bibValue in paperArgs.items():
        if isinstance(bibValue, list):
            for i, item in enumerate(bibValue):
                bibValue[i] = reformat(item)
        elif isinstance(bibValue, str):
            paperArgs[bibKey] = reformat(bibValue)

    # Format date correctly
    year, month, day = paperArgs["datePublished"].split("/")
    paperArgs["datePublished"] = "%s/%s/%s" % (month, day, year)

    return paperArgs
