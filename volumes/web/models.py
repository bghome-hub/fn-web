# models.py

class Citation:
    def __init__(self, id=None, text=''):
        self.id = id
        self.text = text

class Author:
    def __init__(self, id=None):
        self.id = id

class Image:
    def __init__(self, id=None, description='', url=''):
        self.id = id
        self.description = description
        self.url = url

class Article:
    def __init__(self, id=None, topic='', title='', abstract='', introduction='',
                 methodology='', results='', discussion='', conclusion='',
                 citations=None, authors=None, image=None):
        self.id = id
        self.topic = topic

        self.title = title
        self.abstract = abstract
        self.introduction = introduction
        self.methodology = methodology
        self.results = results
        self.discussion = discussion
        self.conclusion = conclusion
        self.image = image
        self.citations = citations if citations is not None else []
        self.authors = authors if authors is not None else []