class Article:
    def __init__(self, prompt, input, title, abstract, intro, methodology, results, discussion, conclusion, article_id=None, authors=None, citations=None, images=None, figures=None):
        self.prompt = prompt  # Store the prompt
        self.input = input
        self.title = title
        self.abstract = abstract
        self.intro = intro
        self.methodology = methodology
        self.results = results
        self.discussion = discussion
        self.conclusion = conclusion
        self.article_id = article_id

        # Initialize lists if none are provided
        self.authors = authors if authors else []
        self.citations = citations if citations else []
        self.images = images if images else []
        self.figures = figures if figures else []
        
    def __repr__(self):
        return f"Article({self.title}, {len(self.authors)} authors, {len(self.citations)} citations)"

class Author:
    def __init__(self, number, name, institution_name, institution_address, email, article_id=None):
        self.number = number
        self.name = name
        self.institution_name = institution_name
        self.institution_address = institution_address
        self.email = email
        self.article_id = article_id

class Citation:
    def __init__(self, number, content, article_id=None):
        self.number = number
        self.content = content
        self.article_id = article_id

class Image:
    def __init__(self, number, description, keywords, url, article_id=None):
        self.number = number
        self.description = description
        self.keywords = keywords
        self.url = url
        self.article_id = article_id

class Figure:
    def __init__(self, number, description, url, article_id=None):
        self.number = number        
        self.description = description
        self.url = url
        self.article_id = article_id