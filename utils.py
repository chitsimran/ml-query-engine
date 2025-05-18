import os
import psycopg2
from config.config import DBConfig, MLModelMapping

def insert_raw_data(folder_path):
    try:
        conn = psycopg2.connect(
            host = DBConfig.HOST,
            database = DBConfig.DATABASE,
            user = DBConfig.USER,
            password = DBConfig.PASSWORD
        )
        cur = conn.cursor()

        for filename in os.listdir(folder_path):
            if "_" in filename:
                try:
                    file_id = int(filename.split('_')[0])
                    file_path = os.path.join(folder_path, filename)

                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    cur.execute(
                        f"INSERT INTO {MLModelMapping.INPUT_TABLE_NAME} (id, data) VALUES (%s, %s)",
                        (file_id, content)
                    )
                except Exception as file_err:
                    print(f"[File Error] {filename}: {file_err}")

        conn.commit()
    except Exception as db_err:
        print(f"[DB Error] {db_err}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()