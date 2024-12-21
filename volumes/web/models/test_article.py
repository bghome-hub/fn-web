from models.article import Article
from models.author import Author
from models.citation import Citation
from models.figure import Figure
from models.image import Image


def create_test_article():
    # Create related objects
    authors = [
        Author(
            guid="author-guid-1",
            name="John Doe",
            institution_name="University of Testing",
            institution_address="123 Test St, Test City, Test Country",
            email="john.doe@test.com"
        ),
        Author(
            guid="author-guid-2",
            name="Jane Smith",
            institution_name="Institute of Testing",
            institution_address="456 Test Ave, Test City, Test Country",
            email="jane.smith@test.com"
        )
    ]

    citations = [
        Citation(
            guid="citation-guid-1",
            content="Doe, J. (2024). Testing in the Modern Era. Journal of Testing, 1(1), 1-10."
        ),
        Citation(
            guid="citation-guid-2",
            content="Smith, J. (2024). Advanced Testing Techniques. Testing Quarterly, 2(2), 20-30."
        )
    ]

    figures = [
        Figure(
            guid="figure-guid-1",
            number=1,
            description="Figure 1: Test Results",
            xaxis_title="X-Axis",
            xaxis_value=10,
            yaxis_title="Y-Axis",
            yaxis_value=20
        ),
        Figure(
            guid="figure-guid-2",
            number=2,
            description="Figure 2: Test Analysis",
            xaxis_title="X-Axis",
            xaxis_value=15,
            yaxis_title="Y-Axis",
            yaxis_value=25
        )
    ]

    images = [
        Image(
            keyword="test-image-1",
            image_id=1
        ),
        Image(
            keyword="test-image-2",
            image_id=2
        )
    ]

    # Create the Article object
    article = Article(
        guid="",
        title="The Importance of Testing",
        journal="Journal of Testing",
        doi="10.1234/testing.2024.001",
        abstract="This article discusses the importance of testing in software development.",
        introduction="Introduction to testing...",
        methodology="Methodology of testing...",
        results="Results of testing...",
        discussion="Discussion on testing...",
        conclusion="Conclusion on testing...",
        keywords="testing, software development, quality assurance",
        user_input="Testing",
        prompt="Write an article about testing.",
        authors=authors,
        citations=citations,
        figures=figures,
        images=images
    )

    return article

# Example usage
if __name__ == "__main__":
    test_article = create_test_article()
    print(test_article)