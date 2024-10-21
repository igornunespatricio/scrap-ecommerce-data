import os
import pyodbc
from dotenv import load_dotenv


class Database:
    def __init__(self):
        # Load environment variables from the .env file
        load_dotenv()

        # Assign the environment variables to class attributes
        self.server = os.getenv("SERVER")
        self.database = os.getenv("DATABASE")
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.driver = os.getenv("DRIVER")

    def connect(self):
        try:
            # Connection string using environment variables
            connection_str = (
                f"DRIVER={self.driver};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
            )
            # Use Windows Authentication if no username/password is provided
            if self.username and self.password:
                connection_str += f"UID={self.username};PWD={self.password}"
            else:
                connection_str += "Trusted_Connection=yes"

            self.conn = pyodbc.connect(connection_str)
            self.cursor = self.conn.cursor()
            print("Database connection successful!")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f"Error executing query: {e}")

    def close(self):
        self.cursor.close()
        self.conn.close()
        print("Database connection closed.")

    def insert_to_bronze(self, product):
        try:
            query = f"""
            INSERT INTO products_bronze (name, price, rating, reviews, category, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?);
            """
            self.cursor.execute(
                query,
                (
                    product["name"],
                    product["price"],
                    product["rating"],
                    product["reviews"],
                    product["category"],
                    product["scraped_at"],
                ),
            )
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting into bronze table: {e}")
