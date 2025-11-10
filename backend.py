import random
import string
import os
from cryptography.fernet import Fernet

KEY_FILE = "key.key"
MASTER_PASSWORD = "abc123D4"
PASSWORD_FILE = "C:/Users/simpl/Projects/password.txt"

# Create or load encryption key
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
else:
    with open(KEY_FILE, "rb") as f:
        key = f.read()

fernet = Fernet(key)
passwords = {}

# Load existing passwords if file exists
if os.path.exists(PASSWORD_FILE):
    with open(PASSWORD_FILE, "r") as file:
        for line in file:
            if ":" in line:
                site, encrypted = line.strip().split(":", 1)
                try:
                    decrypted = fernet.decrypt(encrypted.strip().encode()).decode()
                    passwords[site] = decrypted
                except:
                    print("Warning: Could not decrypt password for", site)

def generate_password(length, capital=True, numbers=True, special=True):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation

    characters = lowercase
    if capital:
        characters += uppercase
    if numbers:
        characters += digits
    if special:
        characters += special_chars

    while True:
        pwd = "".join(random.choice(characters) for _ in range(length))
        if (not capital or any(c in uppercase for c in pwd)) and \
           (not numbers or any(c in digits for c in pwd)) and \
           (not special or any(c in special_chars for c in pwd)):
            return pwd

def save_passwords():
    with open(PASSWORD_FILE, "w") as file:
        for site, pwd in passwords.items():
            encrypted = fernet.encrypt(pwd.encode()).decode()
            file.write(site + ":" + encrypted + "\n")

def add_password():
    site = input("\nWebsite: ")

    if site in passwords:
        print("Password already exists:", passwords[site])
        if input("Overwrite? (y/n): ").lower() != "y":
            return

    try:
        length = int(input("Password Length: "))
    except:
        print("Invalid number.")
        return

    cap = input("Include capital letters? (y/n): ").lower() == "y"
    num = input("Include numbers? (y/n): ").lower() == "y"
    special = input("Include special characters? (y/n): ").lower() == "y"

    pwd = generate_password(length, cap, num, special)
    passwords[site] = pwd
    save_passwords()

    print("\nGenerated Password for", site, ":", pwd)

def view_passwords():
    attempts = 3
    while attempts > 0:
        check = input("\nEnter MASTER PASSWORD: ")
        if check == MASTER_PASSWORD:
            print("\nSaved Passwords:\n")
            for site, pwd in passwords.items():
                print(site, ":", pwd)
            return
        attempts -= 1
        print("Incorrect. Attempts left:", attempts)

    print("Too many attempts. Exiting.")
    exit()

def delete_password():
    site = input("\nWebsite to delete: ").strip()
    if site in passwords:
        if input("Confirm delete? (y/n): ").lower() == "y":
            del passwords[site]
            save_passwords()
            print("Deleted", site)
    else:
        print("Not found.")

def menu():
    while True:
        print("\nMenu:")
        print("1. Add / Generate Password")
        print("2. View Passwords")
        print("3. Delete Password")
        print("4. Exit")

        choice = input("Choose: ")
        if choice == "1":
            add_password()
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            delete_password()
        elif choice == "4":
            print("Exiting")
            exit()
        else:
            print("Invalid.")

print("\nWelcome to the Password Manager!")
menu()

