
import pytest
import uuid  
from datetime import datetime
from Utilities.customLogger import LogGen
from Utilities.db_helper import DbHelper

class TestDatabaseFullSuite:
    logger = LogGen.dbloggen() 

    # =====================================================================================
    # 📑 STEP 1: SHOW ALL TABLES
    # =====================================================================================
    def test_step_1_show_all_tables(self):
        """Step 1: Get list of all tables from database and show in logs"""
        self.logger.info("🔍 --- [STEP 1] Fetching all tables from live Neon DB ---")
        
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        
        # Fix: Call DbHelper query execution using self.db
        results = DbHelper.execute_select_query(self.db, query)
        
        all_tables = [row[0] for row in results] if results else []
        self.logger.info(f"[DB SUCCESS] Total {len(all_tables)} tables found.")
        
        assert len(all_tables) > 0, "❌ FAILED: Database is completely empty!"

    # =====================================================================================
    # 📐 STEP 1.2: SHOW TABLE STRUCTURE
    # =====================================================================================
    def test_step_1_2_show_table_structure(self):
        """Step 1.2: Check columns of users_user table"""
        query = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users_user';"
        
        # Fix: Utilized DbHelper
        columns_structure = DbHelper.execute_select_query(self.db, query)
        
        assert columns_structure is not None
        assert len(columns_structure) > 0

    # =====================================================================================
    # 👥 STEP 2: SELECT LIVE USERS
    # =====================================================================================
    def test_select_user_live(self):
        """Step 2: Read live data from user table"""
        self.logger.info("🔍 --- [STEP 2] Reading the data from users_user table ---")
        
        # Total count query
        count_query = "SELECT COUNT(*) FROM users_user;"
        count_result = DbHelper.execute_select_query(self.db, count_query)
        total_users = count_result[0][0] if count_result else 0

        # Sample data query
        sample_query = "SELECT id, name, email FROM users_user LIMIT 3;"
        live_users_sample = DbHelper.execute_select_query(self.db, sample_query)

        print(f"\n🔥 Live Users Count: {total_users}")
        print(f"🔥 Sample Data: {live_users_sample}\n")
        assert total_users >= 0

    # =====================================================================================
    # 🚀 STEP 3 & 5: INSERT, VERIFY AND CLEANUP (The Ultimate Test)
    # =====================================================================================
    def test_step_3_and_5_insert_and_cleanup_user(self):
        """Step 3 & 5: Insert user, verify insertion, and delete immediately"""
        self.logger.info("🔍 --- [STEP 3] Inserting a dummy user based on live structure ---")

        # 🧪 Dummy data generation
        unique_id = str(uuid.uuid4())
        test_name = "QA Automation Bot 2026"
        test_email = f"automation_bot_{uuid.uuid4().hex[:6]}@shopstack.com"  # Added unique string to ensure unique email
        current_time = datetime.now()

        try:
            # Prepare INSERT query with required columns from live table structure
            insert_query = f"""
                INSERT INTO users_user (id, password, is_superuser, email, name, role, is_active, is_staff, created_at, updated_at)
                VALUES ('{unique_id}', 'FakeHashedPassword123', False, '{test_email}', '{test_name}', 'customer', True, False, '{current_time}', '{current_time}');
            """
            
            # Fix: Call execute_update_or_delete_query to write data
            is_inserted = DbHelper.execute_update_or_delete_query(self.db, insert_query)
            assert is_inserted is True, "❌ FAILED: Query insert operation execution failed!"
            self.logger.info(f"💾 [DB LOG] Dummy user inserted with ID: {unique_id}")

            # 🔎 Verification Check (SELECT)
            verify_query = f"SELECT name, email FROM users_user WHERE id = '{unique_id}';"
            verify_result = DbHelper.execute_select_query(self.db, verify_query)
            
            assert verify_result is not None and len(verify_result) > 0, "❌ FAILED: User could not be inserted (Not found in DB)!"
            assert verify_result[0][0] == test_name, "❌ FAILED: Name mismatch in DB verification!"
            self.logger.info("🟢 [SUCCESS] Data inserted and verified successfully!")

        except Exception as e:
            self.logger.error(f"❌ [DB ERROR] Testing flow interrupted: {e}")
            raise e

        finally:
            # STEP 5: CLEANUP (Always runs to clean up test data)
            self.logger.info(f"[DB LOG] Starting cleanup for test user ID: {unique_id}")
            
            delete_query = f"DELETE FROM users_user WHERE id = '{unique_id}';"
            
            # Fix: Cleanup query run via DbHelper
            is_cleaned = DbHelper.execute_update_or_delete_query(self.db, delete_query)
            
            if is_cleaned:
                self.logger.info("[SUCCESS] Database cleanup complete. Original state restored!\n")
                print("[SUCCESS] Database cleanup complete.")
            else:
                self.logger.error("❌ [CRITICAL WARNING] Cleanup query failed! Stale test data might exist in DB.")