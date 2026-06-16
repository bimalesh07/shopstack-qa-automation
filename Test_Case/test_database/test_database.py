
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
        """Step 1: Database se saari tables ki list nikal kar logs mein show karna"""
        self.logger.info("🔍 --- [STEP 1] Fetching all tables from live Neon DB ---")
        
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        
        # 🔴 FIX: Direct DbHelper ko bola query chalane ko self.db use karke
        results = DbHelper.execute_select_query(self.db, query)
        
        all_tables = [row[0] for row in results] if results else []
        self.logger.info(f"📊 [DB SUCCESS] Total {len(all_tables)} tables mili hain.")
        
        assert len(all_tables) > 0, "❌ FAILED: Database ekdum khali mila!"

    # =====================================================================================
    # 📐 STEP 1.2: SHOW TABLE STRUCTURE
    # =====================================================================================
    def test_step_1_2_show_table_structure(self):
        """Step 1.2: users_user table ke columns check karna"""
        query = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users_user';"
        
        # 🔴 FIX: Utilized DbHelper
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
        """Step 3 & 5: User insert karna, verify karna aur turant delete karna"""
        self.logger.info("🔍 --- [STEP 3] Inserting a dummy user based on live structure ---")

        # 🧪 Dummy data generation
        unique_id = str(uuid.uuid4())
        test_name = "QA Automation Bot 2026"
        test_email = f"automation_bot_{uuid.uuid4().hex[:6]}@shopstack.com"  # Aur unique banane ke liye unique string jodi
        current_time = datetime.now()

        try:
            # 🚀 Live table structure ke required columns ke sath INSERT query taiyar ki
            insert_query = f"""
                INSERT INTO users_user (id, password, is_superuser, email, name, role, is_active, is_staff, created_at, updated_at)
                VALUES ('{unique_id}', 'FakeHashedPassword123', False, '{test_email}', '{test_name}', 'customer', True, False, '{current_time}', '{current_time}');
            """
            
            # 🔴 FIX: Data write karne ke liye execute_update_or_delete_query call kiya
            is_inserted = DbHelper.execute_update_or_delete_query(self.db, insert_query)
            assert is_inserted is True, "❌ FAILED: Query insert operation execution failed!"
            self.logger.info(f"💾 [DB LOG] Dummy user inserted with ID: {unique_id}")

            # 🔎 Verification Check (SELECT)
            verify_query = f"SELECT name, email FROM users_user WHERE id = '{unique_id}';"
            verify_result = DbHelper.execute_select_query(self.db, verify_query)
            
            assert verify_result is not None and len(verify_result) > 0, "❌ FAILED: User insert nahi ho paya (Not found in DB)!"
            assert verify_result[0][0] == test_name, "❌ FAILED: Name mismatch in DB verification!"
            self.logger.info("🟢 [SUCCESS] Data inserted and verified successfully!")

        except Exception as e:
            self.logger.error(f"❌ [DB ERROR] Testing flow interrupted: {e}")
            raise e

        finally:
            #STEP 5: CLEANUP (Har haal mein chalega taaki testing kachra saaf ho jaye)
            self.logger.info(f"[DB LOG] Starting cleanup for test user ID: {unique_id}")
            
            delete_query = f"DELETE FROM users_user WHERE id = '{unique_id}';"
            
            # 🔴 FIX: Cleanup query fired via DbHelper
            is_cleaned = DbHelper.execute_update_or_delete_query(self.db, delete_query)
            
            if is_cleaned:
                self.logger.info("[SUCCESS] Database cleanup complete. Original state restored!\n")
                print("[SUCCESS] Database cleanup complete.")
            else:
                self.logger.error("❌ [CRITICAL WARNING] Cleanup query failed! Stale test data might exist in DB.")