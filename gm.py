#!/usr/bin/env python3
import os
import time
import requests
import itertools
import threading
import random
import string

# --------------------------
# Loading Spinner
# --------------------------
stop_loading = False
def loading(text):
    for frame in itertools.cycle(["•","•","•","•","•","•","•","•","•","•"]):
        if stop_loading:
            break
        print(f"\r{text} {frame}", end="", flush=True)
        time.sleep(0.1)

# --------------------------
# Banner
# --------------------------
def banner():
    os.system("clear")
    print("\033[1;36m" + "="*55)
    print("                     ALEX HUNTER")
    print("             CYBER SENTINEL BANGLADESH")
    print("              WELCOME TO GMAIL GENERATOR")
    print("="*55 + "\033[0m\n")

# --------------------------
# Mail Creation (Mail.tm API)
# --------------------------
def create_mail():
    # Get available domains
    try:
        r = requests.get("https://api.mail.tm/domains").json()
        domain = r["hydra:member"][0]["domain"]
    except Exception as e:
        print(f"\033[1;31mFailed to fetch domain: {e}\033[0m")
        return None, None

    # Generate random username
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    password = "P@ssw0rd123"
    email = f"{username}@{domain}"

    # Create account
    data = {"address": email, "password": password}
    try:
        r = requests.post("https://api.mail.tm/accounts", json=data)
        if r.status_code != 201 and r.status_code != 200:
            print(f"\033[1;31mAccount creation failed: {r.text}\033[0m")
            return None, None

        # Login to get token
        token = requests.post("https://api.mail.tm/token", json=data).json()["token"]
        return email, token
    except Exception as e:
        print(f"\033[1;31mError creating account: {e}\033[0m")
        return None, None

# --------------------------
# OTP Fetcher (10 min) + Auto Save
# --------------------------
def wait_for_otp(mail, token):
    global stop_loading
    headers = {"Authorization": f"Bearer {token}"}
    timeout = time.time() + 600  # 10 minutes
    stop_loading = False

    # Start spinner
    load_thread = threading.Thread(target=loading, args=(f"Waiting for OTP for {mail}",))
    load_thread.start()

    while time.time() < timeout:
        try:
            inbox = requests.get("https://api.mail.tm/messages", headers=headers).json().get("hydra:member", [])
        except:
            inbox = []

        if inbox:
            stop_loading = True
            time.sleep(0.2)
            msg_id = inbox[0]["id"]
            msg = requests.get(f"https://api.mail.tm/messages/{msg_id}", headers=headers).json()
            text = msg.get("text", "")
            otp = None
            for word in text.split():
                if word.isdigit() and len(word) in (4,5,6):
                    otp = word
                    break

            print(f"\n\033[1;32mOTP FOUND for {mail}!\033[0m")
            print("-"*55)
            print(f"Email: \033[1;36m{mail}\033[0m")
            print(f"OTP: \033[1;33m{otp}\033[0m")
            print("-"*55 + "\n")

            # Save to emails.txt
            with open("emails.txt", "a") as f:
                f.write(f"{mail} | OTP: {otp}\n")

            return

        time.sleep(2)

    stop_loading = True
    time.sleep(0.2)
    print(f"\n\033[1;31mOTP NOT RECEIVED for {mail} within 10 minutes.\033[0m\n")

# --------------------------
# Main Program
# --------------------------
banner()
try:
    count = int(input("How many temp-mails do you want to generate?: "))
except:
    print("\033[1;31mInvalid input!\033[0m")
    exit()

for i in range(1, count+1):
    print(f"\n\033[1;36m[ {i} ] Creating Temp Mail...\033[0m")
    mail, token = create_mail()
    if not mail:
        print("\033[1;31mFailed to create mail!\033[0m")
        continue
    wait_for_otp(mail, token)

print("\033[1;32mAll temp-mails processed. OTPs saved in emails.txt\033[0m")