DB_PATH = "data/storage/papers.pkl"

KEYS = {
    'papers': [
        'name',
        'abstract',
        'datePublished',
        'dateAdded',
        'dateRead',
        'link',
        'read',
        'parents',
        'children',
        'notes',
        'authorNames',
        'topicNames',
    ],
    'topic': [
        'name',
        'parents',
        'children',
        'paperNames',
        'authorNames',
    ],
    'author': [
        'name',
        'paperNames',
        'topicNames'
    ]
}
