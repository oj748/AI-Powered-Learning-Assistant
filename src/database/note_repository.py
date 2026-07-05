from database.db import get_connection


def create_note(title, content=""):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO notes(title, content)
        VALUES (?, ?)
        """,
        (title, content)
    )

    conn.commit()
    conn.close()


def get_all_notes():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title
        FROM notes
        ORDER BY title
        """
    )

    notes = cursor.fetchall()

    conn.close()

    return notes


def get_note(note_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM notes
        WHERE id = ?
        """,
        (note_id,)
    )

    note = cursor.fetchone()

    conn.close()

    return note


def update_note(note_id, content):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE notes
        SET
            content = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (content, note_id)
    )

    conn.commit()
    conn.close()


def delete_note(note_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM notes
        WHERE id = ?
        """,
        (note_id,)
    )

    conn.commit()
    conn.close()


def note_exists(title):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM notes
        WHERE title = ?
        """,
        (title,)
    )

    exists = (
        cursor.fetchone()
        is not None
    )

    conn.close()

    return exists

def get_note_titles():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT title
        FROM notes
        ORDER BY title
        """
    )

    notes = [
        row[0]
        for row in cursor.fetchall()
    ]

    conn.close()

    return notes

def append_to_note(title, content):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT content
        FROM notes
        WHERE title = ?
        """,
        (title,)
    )

    row = cursor.fetchone()

    if row:

        updated = (
            row[0]
            + "\n\n"
            + content
        )

        cursor.execute(
            """
            UPDATE notes
            SET
                content = ?,
                updated_at =
                CURRENT_TIMESTAMP
            WHERE title = ?
            """,
            (
                updated,
                title
            )
        )

    conn.commit()

    conn.close()