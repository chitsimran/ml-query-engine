from dotenv import load_dotenv
import os

load_dotenv() 

class DBConfig:
    HOST = 'localhost'
    DATABASE = 'ml-query-engine'
    USER = 'postgres'
    PASSWORD = os.getenv("DB_PASSWORD")

class MLModelMapping:
    INPUT_TABLE_NAME = 'raw_data'
    INPUT_ID_COLUMN = 'id'
    INPUT_DATA_COLUMN = 'data'
    OUTPUT_TABLE_NAME = 'review_analysis'
    OUTPUT_COLUMNS = ['genre', 'is_positive']
