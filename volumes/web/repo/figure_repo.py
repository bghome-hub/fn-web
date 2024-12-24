from dataclasses import dataclass
from typing import Optional, List
import base64
import json

from services import db_service_article as article_db
from models.figure import Figure

# Figure Repository
# This class is responsible for handling all database operations related to the Figure model.
class FigureRepository:
    @staticmethod
    def fetch_by_figure_id(figure_id: int) -> Optional[Figure]:
        '''Fetches a figure from the database by ID.'''
        conn = article_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM figures WHERE figure_id = ?", (figure_id,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None

        return Figure(
            figure_id=row["figure_id"],
            article_id=row["article_id"],
            guid=row["guid"],
            number=row["number"],
            title=row["title"],
            description=row["description"],
            url=row["url"],
            xaxis_title=row["xaxis_title"],
            xaxis_value=json.loads(row["xaxis_value"]),
            yaxis_title=row["yaxis_title"],
            yaxis_value=json.loads(row["yaxis_value"]),
            local=row["local"],
            img_base64=row["img_base64"],
            add_date=row["add_date"]
        )
    
    @staticmethod
    def fetch_all_by_article_id(article_id: int) -> List[Figure]:
        '''Fetches all figures for a given article.'''
        conn = article_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM figures WHERE article_id = ?", (article_id,))
        rows = cursor.fetchall()
        cursor.close()
        figures = []
        for row in rows:
            figures.append(Figure(
                figure_id=row["figure_id"],
                article_id=row["article_id"],
                guid=row["guid"],
                number=row["number"],
                title=row["title"],
                description=row["description"],
                url=row["url"],
                xaxis_title=row["xaxis_title"],
                xaxis_value=json.loads(row["xaxis_value"]),
                yaxis_title=row["yaxis_title"],
                yaxis_value=json.loads(row["yaxis_value"]),
                local=row["local"],
                img_base64=row["img_base64"],
                add_date=row["add_date"]
            ))
        return figures
    
    @staticmethod
    def fetch_all() -> List[Figure]:
        '''Fetches all figures from the database.'''
        conn = article_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM figures")
        rows = cursor.fetchall()
        cursor.close()
        figures = []
        for row in rows:
            figures.append(Figure(
                figure_id=row["figure_id"],
                article_id=row["article_id"],
                guid=row["guid"],
                number=row["number"],
                title=row["title"],
                description=row["description"],
                url=row["url"],
                xaxis_title=row["xaxis_title"],
                xaxis_value=json.loads(row["xaxis_value"]),
                yaxis_title=row["yaxis_title"],
                yaxis_value=json.loads(row["yaxis_value"]),
                local=row["local"],
                img_base64=row["img_base64"],
                add_date=row["add_date"]
            ))
        return figures
    
    @staticmethod
    def insert(figure: Figure) -> None:
        '''Inserts a figure into the database.'''
        conn = article_db.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO figures (article_id, guid, number, title, description, url, xaxis_title, xaxis_value, yaxis_title, yaxis_value, local, img_base64)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            figure.article_id,
            figure.guid,
            figure.number,
            figure.title,
            figure.description,
            figure.url,
            figure.xaxis_title,
            json.dumps(figure.xaxis_value),
            figure.yaxis_title,
            json.dumps(figure.yaxis_value),
            figure.local,
            figure.img_base64
        ))
        conn.commit()
        cursor.close()

    @staticmethod
    def update(figure: Figure) -> None:
        '''Updates a figure in the database.'''
        conn = article_db.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE figures
            SET article_id = ?, guid = ?, number = ?, title = ?, description = ?, url = ?, xaxis_title = ?, xaxis_value = ?, yaxis_title = ?, yaxis_value = ?, local = ?, img_base64 = ?
            WHERE figure_id = ?
        ''', (
            figure.article_id,
            figure.guid,
            figure.number,
            figure.title,
            figure.description,
            figure.url,
            figure.xaxis_title,
            json.dumps(figure.xaxis_value),
            figure.yaxis_title,
            json.dumps(figure.yaxis_value),
            figure.local,
            figure.img_base64,
            figure.figure_id
        ))
        conn.commit()
        cursor.close()

    @staticmethod
    def delete(figure_id: int) -> None:
        '''Deletes a figure from the database.'''
        conn = article_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM figures WHERE figure_id = ?", (figure_id,))
        conn.commit()
        cursor.close()

    