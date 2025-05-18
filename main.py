from dotenv import load_dotenv
import os
from utils import insert_raw_data
from models.groq_model import ask_groq
from process import process_batch
from query import execute

load_dotenv() 

data_path = os.getenv("DATA_PATH")

# Should be run one time only, uncomment to insert data into the database
# insert_raw_data(data_path)

print("Welcome to the ML Query Engine!")
print("This engine allows you to process unstructured data and query the processed results.")
print("Make sure to have your database and Groq model set up correctly.")

while True:
    user_input = input("Enter p to process unstructured data, q to query the processed data, or e to exit: ")
    if user_input.lower() == 'p':
        process_batch()
    elif user_input.lower() == 'q':
        query = input("Enter your SQL query: ")
        print(execute(query))
    elif user_input.lower() == 'e':
        break
    else:
        print("Invalid input. Please try again.")
