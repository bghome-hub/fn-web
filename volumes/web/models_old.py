
    @classmethod
    def create_from_topic(cls, topic):
        ollama_response = ollama.query_ollama(topic)

        # Extract fields safely:
        prompt = ollama_response.get('prompt')
        input_data = ollama_response.get('input')
        title = ollama_response.get('title')
        journal = ollama_response.get('journal')
        doi = ollama_response.get('doi')
        abstract = ollama_response.get('abstract')
        intro = ollama_response.get('introduction')
        methodology = ollama_response.get('methodology')
        results = ollama_response.get('results')
        discussion = ollama_response.get('discussion')
        conclusion = ollama_response.get('conclusion')
        keywords = ollama_response.get('keywords', '')

        authors_data = ollama_response.get('authors', [])
        authors = []
        for i, author_data in enumerate(authors_data):
            authors.append(Author(
                number=i+1,
                name=author_data.get('name', ''),
                institution_name=author_data.get('institution_name', ''),
                institution_address=author_data.get('institution_address', ''),
                email=author_data.get('email', '')
            ))

        citations_data = ollama_response.get('citations', [])
        citations = []
        for i, citation_data in enumerate(citations_data):
            citations.append(Citation(
                number=i+1,
                content=citation_data.get('content', '').strip()
            ))

        return cls(
            title=title,
            journal=journal,
            doi=doi,
            abstract=abstract,
            intro=intro,
            methodology=methodology,
            results=results,
            discussion=discussion,
            conclusion=conclusion,
            keywords=keywords,
            authors=authors,
            citations=citations,
            prompt=prompt,
            input=input_data
        )

    @classmethod
    def load_from_db(cls, id: int) -> Optional['Article']:
        row = db.get_article_by_id(id)
        if not row:
            return None

        article = cls._from_row(row)
        article._load_related_data()
        return article

    def save_to_db(self):
        self.id = db.insert_article(self)
        
        for author in self.authors:
            author.article_id = self.id
            author.save_to_db()

        for citation in self.citations:
            citation.article_id = self.id
            citation.save_to_db()

        for image in self.images:
            image.article_id = self.id
            image.save_to_db()

        for figure in self.figures:
            figure.article_id = self.id
            figure.save_to_db()

        return self

    @classmethod
    # Get an article by its ID
    def get_by_id(cls, id: int) -> Optional['Article']:
        row = db.get_article_by_id(id)
        if not row:
            return None
        
        article = cls._from_row(row)
        article._load_related_data()
        
        return article
 
    @classmethod
    def _from_row(cls, row) -> 'Article':
        """Create an Article object from a database row."""
        return cls(
            id=row["id"],
            title=row["title"],
            journal=row["journal"],
            doi=row["doi"],
            abstract=row["abstract"],
            intro=row["intro"],
            methodology=row["methodology"],
            results=row["results"],
            discussion=row["discussion"],
            conclusion=row["conclusion"],
            keywords=row["keywords"],
            prompt=row["prompt"],
            input=row["input"],
            add_date=row["add_date"],
            update_date=row["update_date"]
        )

    # Load related data for the article
    def _load_related_data(self):
        """Load related data for the article."""
        self.authors = Author.get_by_article_id(self.id)
        self.citations = Citation.get_by_article_id(self.id)
        self.images = Image.get_by_article_id(self.id)
        self.figures = Figure.get_by_article_id(self.id)

    @classmethod
    def get_all(cls) -> List['Article']:
        """Create an Article object from a database row."""
        
        rows = db.get_all_articles()
        articles = []

        for row in rows:
            article = cls._from_row(row)
            article._load_related_data()
            articles.append(article)
        return articles

    @classmethod
    def count(cls) -> int:
        """Get the count of articles."""
        return db.get_count_of_articles()

    @classmethod
    def get_last_x_articles(cls, x: int) -> List['Article']:
        """Get the last x articles."""
        
        rows = db.get_last_x_articles(x)
        articles = []
        
        for row in rows:
            article = cls._from_row(row)
            article._load_related_data()
            articles.append(article)
        return articles

    # search for image based on my keywords parameter
    def search_image(self):
        image = Image.search(self.keywords, self.id)
        if image:
            self.images.append(image)
            return image
        return None


class Author:
    def __init__(self, number, name, institution_name, institution_address, email, article_id=None):
        self.number = number
        self.name = name
        self.institution_name = institution_name
        self.institution_address = institution_address
        self.email = email
        self.article_id = article_id

    def save_to_db(self):
        db.insert_author(self)

    @classmethod
    def get_by_article_id(cls, article_id):
        rows = db.get_authors_by_article_id(article_id)
        authors = []
        for row in rows:
            authors.append(cls(
                number=row["number"],
                name=row["name"],
                institution_name=row["institution_name"],
                institution_address=row["institution_address"],
                email=row["email"],
                article_id=row["article_id"]
            ))
        return authors

class Citation:
    def __init__(self, number, content, article_id=None):
        self.number = number
        self.content = content
        self.article_id = article_id

    def save_to_db(self):
        db.insert_citation(self)

    @classmethod
    def get_by_article_id(cls, article_id):
        rows = db.get_citations_by_article_id(article_id)
        citations = []
        for row in rows:
            citations.append(cls(
                number=row["number"],
                content=row["content"],
                article_id=row["article_id"]
            ))
        return citations

# If article ID was passed, then the image is associated with the article

class Image:
    def __init__(self, number, description, keywords, url, local, article_id=None):
        self.number = number
        self.description = description
        self.keywords = keywords
        self.url = url
        self.local = local
        self.article_id = article_id

    def __repr__(self):
        return f"Image({self.url})"

    # Save the image to the database
    def save_to_db(self):
        db.insert_image(self)

    # Fetches the URL of an image based on the keywords and save to object
    @classmethod
    def search(cls, keywords, article_id) -> Optional['Image']:
        """Fetches the URL of an image based on the keywords."""
        params = {
            "query": keywords,
            "per_page": 1,  # Only fetch one result to ensure top relevance
            "page": 1
        }
        headers = {
            "Authorization": f"Client-ID {IMAGE_API_KEY}"
        }

        # Make the request to the image API
        response = requests.get(IMAGE_URL, headers=headers, params=params)
        response.raise_for_status()

        # Get the image URL and description
        data = response.json()
        results = data.get("results", [])
        if not results:
            return None
        
        # Get the image URL and description
        image_info = results[0]
        image_url = image_info["urls"]["regular"]
        description = image_info.get("description")

        # create image object and populate with data
        image = cls(
            number=None,
            description=description,
            keywords=keywords,
            url=image_url,
            local=0,
            article_id=article_id
        )

        return image    

    @classmethod
    def get_by_article_id(cls, article_id):
        rows = db.get_images_by_article_id(article_id)
        images = []
        for row in rows:
            images.append(cls(
                number=row["number"],
                description=row["description"],
                keywords=row["keywords"],
                url=row["url"],
                local=row["local"],
                article_id=row["article_id"]
            ))
        return images

class Figure:
    def __init__(self, number, description, url, article_id=None):
        self.number = number
        self.description = description
        self.url = url
        self.article_id = article_id

    def save_to_db(self):
        db.insert_figure(self)

    @classmethod
    def get_by_article_id(cls, article_id):
        rows = db.get_figures_by_article_id(article_id)
        figures = []
        for row in rows:
            figures.append(cls(
                number=row["number"],
                description=row["description"],
                url=row["url"],
                article_id=row["article_id"]
            ))
        return figures
