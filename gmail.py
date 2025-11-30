import os
from dotenv import load_dotenv

load_dotenv()  # load .env file

real_pass = os.getenv("GM_PASS")

if not real_pass:
    print("Password not set! (.env file missing)")
    exit()

user_pass = input("Enter password: ")

if user_pass != real_pass:
    print("Wrong password!")
    exit()

print("Access Granted!")
