DB_PATH = "data/storage/papers.pkl"

KEYS = {
    "papers": [
        "name",
        "abstract",
        "datePublished",
        "dateAdded",
        "dateRead",
        "link",
        "read",
        "parents",
        "children",
        "notes",
        "authorNames",
        "topicNames",
    ],
    "topics": ["name", "parents", "children", "paperNames", "authorNames",],
    "authors": ["name", "paperNames", "topicNames"],
}
