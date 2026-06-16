# 👉 File Location: Test_Case/test_database/conftest.py
import os
import pytest
import psycopg2
from dotenv import load_dotenv
from Utilities.customLogger import LogGen

# Path setup: 3 folder peeche jaakar main project root se .env file ko load karega
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path=env_path)

logger = LogGen.loggen()

# =====================================================================================
# 🗄️ DATABASE FIXTURE (AUTOMATIC CLASS-LEVEL INJECTION)
# =====================================================================================
@pytest.fixture(scope="class", autouse=True)
def db_session(request):
    """
    Cloud Neon Postgres Database Connection Fixture.
    Yeh parde ke peeche se automatic har test class ko 'self.db' thama dega.
    """
    connection = None
    logger.info("\n⏳ --- [DB CONNECT] Connecting to Cloud Neon Postgres Database... ---")
    print("\n⏳ --- [DB CONNECT] Connecting to Cloud Neon Postgres Database... ---")
    
    try:
        connection = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            port=os.environ.get("DB_PORT", "5432"),
            sslmode='require'  # Neon Cloud ke liye mandatory hai
        )
        logger.info("[DB SUCCESS] Connected successfully with Cloud Neon Database!")
        print("[DB SUCCESS] Connected successfully with Cloud Neon Database!")
        
        # ASLI JADU: Connection object ko seedhe test class ke andar 'db' variable bana kar daal diya
        if request.cls is not None:
            request.cls.db = connection
            
        yield connection  # Yahan par aakar pause hoga aur test cases ko chalne dega
        
    except Exception as db_err:
        # 🔴 FIX: logger.error kiya taaki crash na ho
        logger.error(f"\n❌ [DB CRITICAL ERROR] Neon cloud connection failed: {db_err}")
        raise db_err
        
    finally:
        # FINALLY BLOCK: Safe closing
        if connection is not None:
            connection.close()
            logger.info("🔌 [DB TEARDOWN] Cloud Neon Connection safely closed.")
            print("🔌 [DB TEARDOWN] Cloud Neon Connection safely closed.")