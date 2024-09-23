import psycopg2
from data import *
from config import *


try:
    # Connect to PostgreSQL database
    connection = psycopg2.connect(
        host=HOST, 
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        port=PORT  
    )
    # Create a cursor object
    cursor = connection.cursor()
    update_data(connection,cursor)
except Exception as e:
    print(e)

