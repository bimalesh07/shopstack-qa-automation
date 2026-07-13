import pytest
import uuid  
from datetime import datetime
from Utilities.customLogger import LogGen
from Utilities.db_helper import DbHelper

class TestDatabaseFullSuite:
    logger = LogGen.dbloggen() 

    def test_step_1_show_all_tables(self):
        self.logger.info("Fetching all tables from live database schema")
        
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        results = DbHelper.execute_select_query(self.db, query)
        
        all_tables = [row[0] for row in results] if results else []
        self.logger.info(f"Database query complete: Total {len(all_tables)} tables identified.")
        
        assert len(all_tables) > 0, "Validation check failed: Database schema is completely empty."

    def test_step_1_2_show_table_structure(self):
        self.logger.info("Validating schema column structure for table users_user")
        query = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users_user';"
        
        columns_structure = DbHelper.execute_select_query(self.db, query)
        
        assert columns_structure is not None, "Column structure schema returned None."
        assert len(columns_structure) > 0, "Column metadata collection is empty."

    def test_select_user_live(self):
        self.logger.info("Reading existing data records from users_user table")
        
        count_query = "SELECT COUNT(*) FROM users_user;"
        count_result = DbHelper.execute_select_query(self.db, count_query)
        total_users = count_result[0][0] if count_result else 0

        sample_query = "SELECT id, name, email FROM users_user LIMIT 3;"
        live_users_sample = DbHelper.execute_select_query(self.db, sample_query)

        self.logger.info(f"Active records metrics: Live Users Count = {total_users}")
        self.logger.info(f"Data sampling dump: {live_users_sample}")
        assert total_users >= 0

    def test_step_3_and_5_insert_and_cleanup_user(self):
        self.logger.info("Inserting mock entity record based on schema constraints")

        unique_id = str(uuid.uuid4())
        test_name = "QA Automation Bot 2026"
        test_email = f"automation_bot_{uuid.uuid4().hex[:6]}@shopstack.com"  
        current_time = datetime.now()

        try:
            insert_query = f"""
                INSERT INTO users_user (id, password, is_superuser, email, name, role, is_active, is_staff, created_at, updated_at)
                VALUES ('{unique_id}', 'FakeHashedPassword123', False, '{test_email}', '{test_name}', 'customer', True, False, '{current_time}', '{current_time}');
            """
            
            is_inserted = DbHelper.execute_update_or_delete_query(self.db, insert_query)
            assert is_inserted is True, "Record insertion execution failed."
            self.logger.info(f"Mock record injected successfully with ID: {unique_id}")

            # Verification Phase
            verify_query = f"SELECT name, email FROM users_user WHERE id = '{unique_id}';"
            verify_result = DbHelper.execute_select_query(self.db, verify_query)
            
            assert verify_result is not None and len(verify_result) > 0, " Target record not found in persistence layer."
            assert verify_result[0][0] == test_name, " Data payload property mismatch on name field."
            self.logger.info("Data validation confirmed successfully.")

        except Exception as e:
            self.logger.error(f"Execution flow exception encountered: {e}")
            raise e

        finally:
            # Cleanup Phase
            self.logger.info(f"Initializing automated lifecycle cleanup for entity ID: {unique_id}")
            delete_query = f"DELETE FROM users_user WHERE id = '{unique_id}';"
            
            is_cleaned = DbHelper.execute_update_or_delete_query(self.db, delete_query)
            
            if is_cleaned:
                self.logger.info("Cleanup executed successfully and baseline state restored.")
            else:
                self.logger.error("Cleanup script execution failed. Orphan records may exist.")