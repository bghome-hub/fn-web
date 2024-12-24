from services import db_service_article as article_db
from services import db_service_story as story_db

def ensure_tables_created():
    if not hasattr(article_db, 'tables_created'):
        article_db.create_tables()
        article_db.tables_created = True

    if not hasattr(story_db, 'tables_created'):
        story_db.create_tables()
        story_db.tables_created = True

        