
import os

import psycopg
from dotenv import load_dotenv


# Read credentials from .env file
load_dotenv()


# Function to connect Python with PostgreSQL
def get_connection():

    connection = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    return connection


# Test database connection
if __name__ == "__main__":

    try:
        with get_connection() as conn:

            with conn.cursor() as cursor:

                cursor.execute(
                    "SELECT vehicle_id, model, version, status "
                    "FROM vehicles ORDER BY vehicle_id"
                )

                vehicles = cursor.fetchall()

                print("\nDatabase Connected Successfully!")
                print("\nRegistered Vehicles:\n")

                for vehicle in vehicles:
                    print(vehicle)

    except psycopg.Error as error:
        print("\nDatabase Connection Failed!")
        print("Error:", error)
