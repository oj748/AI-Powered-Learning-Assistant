from database.db import get_connection

from datetime import datetime, timedelta

# ==========================
# Decks
# ==========================

def create_deck(name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO decks(name)
        VALUES (?)
        """,
        (name,)
    )

    conn.commit()
    conn.close()


def get_all_decks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name
        FROM decks
        ORDER BY name
        """
    )

    decks = cursor.fetchall()

    conn.close()

    return decks


def delete_deck(deck_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM decks
        WHERE id = ?
        """,
        (deck_id,)
    )

    conn.commit()
    conn.close()


# ==========================
# Flashcards
# ==========================

def create_flashcard(deck_id, front,back):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO flashcards(
            deck_id,
            front,
            back
        )
        VALUES (?, ?, ?)
        """,
        (
            deck_id,
            front,
            back
        )
    )

    conn.commit()
    conn.close()

def get_flashcards_for_deck(deck_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM flashcards
        WHERE deck_id = ?
        ORDER BY id
        """,
        (deck_id,)
    )

    flashcards = cursor.fetchall()

    conn.close()

    return flashcards

def delete_flashcards(ids):

    conn = get_connection()
    cursor = conn.cursor()

    placeholders = ",".join("?" * len(ids))

    cursor.execute(
        f"""
        DELETE FROM flashcards
        WHERE id IN ({placeholders})
        """,
        ids
    )

    conn.commit()
    conn.close()


def update_review(flashcard_id,interval_days,ease_factor,review_count,next_review):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE flashcards
        SET
            interval_days = ?,
            ease_factor = ?,
            review_count = ?,
            last_review = datetime('now','localtime'),
            next_review = ?
        WHERE id = ?
        """,
        (
            interval_days,
            ease_factor,
            review_count,
            next_review,
            flashcard_id
        )
    )

    conn.commit()
    conn.close()

def get_due_flashcards_for_deck(deck_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM flashcards
        WHERE deck_id = ?
        AND datetime(next_review)
            <= datetime('now','localtime')
        ORDER BY next_review
        """,
        (deck_id,)
    )

    cards = cursor.fetchall()

    conn.close()

    return cards

def flashcard_exists(deck_id,front):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM flashcards
        WHERE deck_id = ?
        AND front = ?
        """,
        (
            deck_id,
            front
        )
    )

    exists = (
        cursor.fetchone()
        is not None
    )

    conn.close()

    return exists

def create_flashcard_if_missing(deck_id,front,back):

    if flashcard_exists(
            deck_id,
            front
    ):
        return False

    create_flashcard(
        deck_id,
        front,
        back
    )

    return True

def get_deck_id_by_name(name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM decks
        WHERE name = ?
        """,
        (name,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None

def update_flashcard_review(flashcard_id,rating):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            interval_days,
            ease_factor,
            review_count
        FROM flashcards
        WHERE id = ?
        """,
        (flashcard_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if not row:
        return

    interval = row[0] or 0
    ease = row[1] or 2.5
    reviews = row[2] or 0

    # AGAIN
    if rating == 0:

        interval = 0
        reviews = 0
        ease = max(1.3, ease - 0.2)

        next_review = datetime.now()

    # HARD
    elif rating == 1:

        reviews += 1

        interval = max(
            1,
            int(interval * 1.2)
        )

        ease = max(
            1.3,
            ease - 0.15
        )

        next_review = (
            datetime.now()
            + timedelta(days=interval)
        )

    # GOOD
    elif rating == 2:

        if reviews == 0:
            interval = 1

        elif reviews == 1:
            interval = 3

        else:
            interval = max(
                1,
                int(interval * ease)
            )

        reviews += 1

        next_review = (
            datetime.now()
            + timedelta(days=interval)
        )

    # EASY
    else:

        if reviews == 0:
            interval = 4

        else:
            interval = max(
                4,
                int(interval * ease * 1.3)
            )

        reviews += 1
        ease += 0.15

        next_review = (
            datetime.now()
            + timedelta(days=interval)
        )

    update_review(
        flashcard_id,
        interval,
        ease,
        reviews,
        next_review.strftime("%Y-%m-%d %H:%M:%S")
    )

def get_deck_statistics(deck_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(
                CASE
                    WHEN datetime(next_review)
                        <= datetime('now','localtime')
                    THEN 1
                    ELSE 0
                END
            ),
            AVG(ease_factor)
        FROM flashcards
        WHERE deck_id = ?
    """, (deck_id,))

    stats = cursor.fetchone()

    conn.close()

    return (
        stats[0] or 0,
        stats[1] or 0,
        round(stats[2] or 2.5, 2)
    )