import psycopg2
from models.groq_model import ask_groq_to_parse_movie_review
from config.config import MLModelMapping, DBConfig

def process_batch():
    """
    Process a batch of raw data from the database, send it to the Groq model for analysis,
    and store the results in the database.
    """
    conn = psycopg2.connect(
        host = DBConfig.HOST,
        database = DBConfig.DATABASE,
        user = DBConfig.USER,
        password = DBConfig.PASSWORD
    )

    cursor = conn.cursor()

    while True:
        cursor.execute(f"""
            SELECT r.{MLModelMapping.INPUT_ID_COLUMN}, r.{MLModelMapping.INPUT_DATA_COLUMN}
            FROM {MLModelMapping.INPUT_TABLE_NAME} r
            LEFT JOIN processed_results p ON r.{MLModelMapping.INPUT_ID_COLUMN} = p.raw_data_id
            WHERE p.raw_data_id IS NULL
            LIMIT 10;
        """)
        rows = cursor.fetchall()
        if not rows:
            print("All rows processed.")
            break

        for row_id, text in rows:
            try:
                response = ask_groq_to_parse_movie_review(text)
                if ',' not in response:
                    continue
                (genre, sentiment) = response.split(",")
                is_positive = True if sentiment.strip().lower().replace(" ", "") == "positive" else False
                print(f"[{row_id}] → {response}")

                cursor.execute(
                    "INSERT INTO processed_results (raw_data_id, processed) VALUES (%s, TRUE)",
                    (row_id,)
                )

                cursor.execute(
                    f"INSERT INTO {MLModelMapping.OUTPUT_TABLE_NAME} (raw_data_id, genre, is_positive) VALUES (%s, %s, %s) ON CONFLICT (raw_data_id) DO NOTHING",
                    (row_id, genre.strip(), is_positive)
                )
                conn.commit()
                break

            except Exception as e:
                print(f"Error processing row {row_id}: {e}")
                if "rate limit" in str(e).lower():
                    print("Rate limit hit. Exiting...")
                    break
                else:
                    print(f"Some other error occurred. Breaking regardless... {e}")
                    break

    cursor.close()
    conn.close()
