# 👉 File Location: Utilities/Db_helper.py
from Utilities.customLogger import LogGen

class DbHelper:
    logger = LogGen.loggen()

    @staticmethod
    def execute_select_query(connection, query):
        """🔎 SELECT Query chalakar data list laane ke liye"""
        cursor = None
        try:
            # Bane-banaye connection se cursor banaya
            cursor = connection.cursor()
            DbHelper.logger.info(f"💾 Executing DB Query: {query}")
            
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            DbHelper.logger.error(f"❌ SQL Select Error: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def execute_update_or_delete_query(connection, query):
        """🛠️ INSERT, UPDATE, ya DELETE query chalane ke liye"""
        cursor = None
        try:
            cursor = connection.cursor()
            DbHelper.logger.info(f"💾 Executing DB Write Query: {query}")
            
            cursor.execute(query)
            connection.commit()  # Changes pakke karne ke liye
            return True
        
        except Exception as e:
            DbHelper.logger.error(f"❌ SQL Write Error: {e}")
            connection.rollback()  # Galti hone par purana roll back karne ke liye
            return False
        finally:
            if cursor:
                cursor.close()