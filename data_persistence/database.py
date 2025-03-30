import psycopg2
from psycopg2 import pool
import logging
import json
from contextlib import contextmanager
from .models import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection pool
db_pool = None

def initialize_db_pool(minconn=1, maxconn=10):
    """Initialize the PostgreSQL connection pool."""
    global db_pool
    db_pool = psycopg2.pool.SimpleConnectionPool(
        minconn,
        maxconn,
        dbname="mydatabase",
        user="myuser",
        password="mypassword",
        host="localhost",
        port="5432"
    )
    logger.info("Database connection pool initialized.")

@contextmanager
def get_db_connection():
    """Context manager for getting a database connection from the pool."""
    conn = db_pool.getconn()
    try:
        yield conn
    finally:
        db_pool.putconn(conn)

async def save_state_change(entity_id, entity_type, state, user):
    """Save a state change to the database asynchronously.

    Args:
        entity_id (str): The ID of the entity that was changed.
        entity_type (str): The type of the entity that was changed.
        state (dict): The new state of the entity.
        user (User): The user who made the state change.
    """
    state_json = json.dumps(state)  # Convert state dict to JSON string
    try:
        async with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO statechange (entity_id, entity_type, state, user_id) VALUES (%s, %s, %s, %s)",
                    (entity_id, entity_type, state_json, user.id)
                )
                conn.commit()
                logger.info(f"State change saved for entity_id: {entity_id}, entity_type: {entity_type}.")
    except Exception as e:
        logger.error(f"Error saving state change: {e}")

async def get_state_history(entity_id, entity_type):
    """Get the state history for a given entity asynchronously.

    Args:
        entity_id (str): The ID of the entity.
        entity_type (str): The type of the entity.

    Returns:
        A list of state changes for the given entity.
    """
    try:
        async with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM statechange WHERE entity_id = %s AND entity_type = %s ORDER BY timestamp",
                    (entity_id, entity_type)
                )
                rows = cur.fetchall()

        state_changes = []
        for row in rows:
            state_changes.append({
                "entity_id": row[1],
                "entity_type": row[2],
                "state": json.loads(row[3]),  # Convert JSON string back to dict
                "user": User.objects.get(id=row[4]),
                "timestamp": row[5]
            })

        logger.info(f"Retrieved state history for entity_id: {entity_id}, entity_type: {entity_type}.")
        return state_changes
    except Exception as e:
        logger.error(f"Error retrieving state history: {e}")
        return []

# Initialize the database connection pool at the start of your application
initialize_db_pool()
