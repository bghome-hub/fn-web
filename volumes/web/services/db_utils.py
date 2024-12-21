from services import db_service as db

def ensure_tables_created():
    if not hasattr(db, 'tables_created'):
        db.create_tables()
        db.tables_created = True
