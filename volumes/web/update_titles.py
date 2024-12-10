from titlecase import titlecase
import sqlite3
import os

# Configuration
DB_FILE = os.getenv("DB_FILE", "/db/db.db")  # Ensure this path matches your setup

def update_titles():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Fetch all articles with their current titles and topics
        cursor.execute('SELECT id, topic, title FROM articles')
        articles = cursor.fetchall()

        print(f"Found {len(articles)} articles in the database.")

        # Counter for updated records
        updated_count = 0

        for article in articles:
            article_id, topic, current_title = article

            # Generate the new title using titlecase
            new_title = titlecase(topic)

            # Check if the current title already matches the new title to avoid unnecessary updates
            if current_title != new_title:
                # Update the title in the database
                cursor.execute('''
                    UPDATE articles
                    SET title = ?
                    WHERE id = ?
                ''', (new_title, article_id))
                updated_count += 1
                print(f"Updated Article ID {article_id}: '{current_title}' -> '{new_title}'")
            else:
                print(f"Article ID {article_id} already has the correct title: '{current_title}'")

        # Commit the changes
        conn.commit()
        conn.close()

        print(f"\nTitle update completed. {updated_count} out of {len(articles)} articles were updated.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as ex:
        print(f"An error occurred: {ex}")

if __name__ == "__main__":
    update_titles()
