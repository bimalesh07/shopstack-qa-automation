# 👉 File Location: Utilities/customLogger.py
import logging
import os

class LogGen:

    # 🖥️ 1. THIS IS FOR UI TESTING (Normal/Default Logs)
    @staticmethod
    def loggen():
        if not os.path.exists(".\\Logs"):
            os.makedirs(".\\Logs")
        logger = logging.getLogger("ShopStackAutomation")
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.setLevel(logging.INFO)
        
        file_handler = logging.FileHandler(".\\Logs\\automation.log", mode='a', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    # 🌐 2. THIS IS FOR API TESTING (Perfect Name)
    @staticmethod
    def apiloggen():  # 👈 Iska naam ab sahi se 'apiloggen' hai
        if not os.path.exists(".\\Logs"):
            os.makedirs(".\\Logs")
            
        api_logger = logging.getLogger("ShopStackAPI") 
        if api_logger.hasHandlers():
            api_logger.handlers.clear()
        api_logger.setLevel(logging.INFO)
        
        api_file_handler = logging.FileHandler(".\\Logs\\automation_api.log", mode='a', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        api_file_handler.setFormatter(formatter)
        api_logger.addHandler(api_file_handler)
        return api_logger
    
    # 🗄️ 3.HIS IS FOR DATABASE TESTING (Perfect Name)
    @staticmethod
    def dbloggen():  # 👈 Iska naam ab sahi se 'dbloggen' hai
        if not os.path.exists(".\\Logs"):
            os.makedirs(".\\Logs")
            
        db_logger = logging.getLogger("Db_Shopstack_Testing") 
        if db_logger.hasHandlers():
            db_logger.handlers.clear()
        db_logger.setLevel(logging.INFO)
        
        db_file_handler = logging.FileHandler(".\\Logs\\Db_Testing.log", mode='a', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        db_file_handler.setFormatter(formatter)
        db_logger.addHandler(db_file_handler)
        return db_logger