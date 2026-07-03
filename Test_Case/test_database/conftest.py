import os
import pytest
import psycopg2
from dotenv import load_dotenv
from Utilities.customLogger import LogGen

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path=env_path)

logger = LogGen.loggen()

@pytest.fixture(scope="class", autouse=True)
def db_session(request):
    """
    Class-level fixture to initialize and manage Cloud Neon Postgres Database connection.
    Automatically injects the active connection instance into the test class context.
    """
    connection = None
    logger.info("Initializing connection sequence to Cloud Neon Postgres Database.")
    
    try:
        connection = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            port=os.environ.get("DB_PORT", "5432"),
            sslmode='require'
        )
        logger.info("Database handshake successful: Connected to Cloud Neon repository.")
        
        if request.cls is not None:
            request.cls.db = connection
            
        yield connection
        
    except Exception as db_err:
        logger.error(f"Critical connection failure encountered during database initialization: {db_err}")
        raise db_err
        
    finally:
        if connection is not None:
            connection.close()
            logger.info("Database teardown complete: Cloud Neon session safely closed.")