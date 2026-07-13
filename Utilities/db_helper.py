
from Utilities.customLogger import LogGen

class DbHelper:
    logger = LogGen.dbloggen()

    @staticmethod
    def execute_select_query(connection, query):
        cursor = None
        try:
            # Create cursor from the connection
            cursor = connection.cursor()
            DbHelper.logger.info(f" Executing DB Query: {query}")
            
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            DbHelper.logger.error(f"SQL Select Error: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def execute_update_or_delete_query(connection, query):
        """Execute INSERT, UPDATE, or DELETE query"""
        cursor = None
        try:
            cursor = connection.cursor()
            DbHelper.logger.info(f"Executing DB Write Query: {query}")
            
            cursor.execute(query)
            connection.commit()  # Commit transaction
            return True
        
        except Exception as e:
            DbHelper.logger.error(f"SQL Write Error: {e}")
            connection.rollback()  # Rollback on error
            return False
        finally:
            if cursor:
                cursor.close()