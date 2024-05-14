import psycopg2

from .models import StateChange


def connect_to_database():
    """Connect to the PostgreSQL database.

    Returns:
        A PostgreSQL database connection object.
    """
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="myuser",
        password="mypassword",
        host="localhost",
        port="5432",
    )
    return conn


def save_state_change(entity_id, entity_type, state, user):
    """Save a state change to the database.

    Args:
        entity_id (str): The ID of the entity that was changed.
        entity_type (str): The type of the entity that was changed.
        state (dict): The new state of the entity.
        user (User): The user who made the state change.
    """
    with connect_to_database() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO statechange (entity_id, entity_type, state, user_id) VALUES (%s, %s, %s, %s)",
                (entity_id, entity_type, state, user.id),
            )
            conn.commit()


def get_state_history(entity_id, entity_type):
    """Get the state history for a given entity.

    Args:
        entity_id (str): The ID of the entity.
        entity_type (str): The type of the entity.

    Returns:
        A list of state changes for the given entity.
    """
    with connect_to_database() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM statechange WHERE entity_id = %s AND entity_type = %s ORDER BY timestamp",
                (entity_id, entity_type),
            )
            rows = cur.fetchall()

    state_changes = []
    for row in rows:
        state_changes.append(
            {
                "entity_id": row[1],
                "entity_type": row[2],
                "state": row[3],
                "user": User.objects.get(id=row[4]),
                "timestamp": row[5],
            }
        )

    return state_changes
