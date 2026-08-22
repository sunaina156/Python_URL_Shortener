import random
import string

# Dictionary used to store short code and original URL
url_storage = {}

def generate_short_code():
    characters = string.ascii_letters + string.digits

    code = ""    # start with an empty string

    for _ in range(6):   # run this loop 6 times
        code += random.choice(characters)   # each time choose 1 random character
    return code



# create a function that takes the original URL and stores it with the generated short code.
# This function takes the original/long URL as input
def store_url(original_url):

    # call the generate_short_code function
    # It creates a random short code, for ex: "aB72xQ"
    short_code = generate_short_code()

    # store the original URL using the short code as the key so dictionary becomes { "short_code": "long_url"}
    while short_code in url_storage:
         short_code = generate_short_code()
    url_storage[short_code] = original_url

    # return the generated short code
    # This allows us to use the short code outisde this function
    return short_code


#---------------

# Retrieve the Original URL
def get_original_url(short_code):
        if short_code in url_storage:
            return url_storage[short_code]
        else:
             return "Short code not found!"

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
          short_code = store_url(original_url)
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