import random
import string
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def get_connection():
     return psycopg2.connect(
          host=os.getenv("DB_HOST"),
          database=os.getenv("DB_NAME"),
          user=os.getenv("DB_USER"),
          password=os.getenv("DB_PASSWORD"),
          port =os.getenv("DB_PORT")
     )



def generate_short_code():
    characters = string.ascii_letters + string.digits

    code = ""    # start with an empty string

    for _ in range(6):   # run this loop 6 times
        code += random.choice(characters)   # each time choose 1 random character
    return code



# create a function that takes the original URL and stores it with the generated short code.
# This function takes the original/long URL as input
def store_url(original_url, user_id):

    connection = get_connection()
    cursor = connection.cursor()   # A cursor is what you use to send SQL commands to PostgreSQL.

    short_code = generate_short_code()

    cursor.execute(
         """
         INSERT INTO urls (short_code, original_url, user_id)
         VALUES (%s, %s, %s)
         RETURNING short_code;
         """,
         (short_code, original_url, user_id)
    )

    short_code = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return short_code

#---------------

# Retrieve the Original URL
def get_original_url(short_code):

    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT id, original_url
        FROM urls
        WHERE short_code = %s;
        """,
        (short_code,)
    )

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        url_id = result[0]
        original_url = result[1]

        record_click(url_id)  
        return original_url
    else:
        return "Short code not found!"


# Add Click Tracing Function
def record_click(url_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO clicks (url_id)
        VALUES(%s);
        """,
        (url_id,)
    )

    connection.commit()
    cursor.close()
    connection.close()

#-----------------------
# Menu
while True:
     print("\n==============================")
     print("             URL SHORTENER")
     print("==============================")
     print("1. Shorten URL")
     print("2. Retrieve Original URL")
     print("3. Exit")

     choice = input("Enter your choice: ")

     if choice == "1":
          original_url = input("Enter the URL you want to shorten: ")
          short_code = store_url(original_url, 1)
          print("Short Code: ", short_code)

     elif choice == "2":
        entered_code = input("Enter the short code: ")
        original_url = get_original_url(entered_code)
        print("Original URL:", original_url)

     elif choice == "3":
          print("Goodbye!")
          break

     else:
          print("Invalid choice! Please select 1, 2, or 3.")


# ---------------------

