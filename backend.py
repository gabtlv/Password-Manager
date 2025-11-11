import random
import string
import os
from cryptography.fernet import Fernet

KEY_FILE = "key.key"
MASTER_PASSWORD = "admin123"

if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
else:
    with open(KEY_FILE, "rb") as key_file:
        key = key_file.read()

fernet = Fernet(key)

passwords = {}

if os.path.exists("C:/Users/simpl/Projects/password.txt"):
    with open("C:/Users/simpl/Projects/password.txt", "r") as file:
        for line in file:
            if ":" in line:
                website, encrypted = line.strip().split(":", 1)
                try:
                    decrypted = fernet.decrypt(encrypted.strip().encode()).decode()
                    passwords[website] = decrypted
                except:
                    print("Warning: Cannot decrypt password for " + website)

def add_password():
    website = input("\nWhat website is this password for? ").strip()
    if website in passwords:
        print("Password for " + website + " already exists: " + passwords[website])
        overwrite = input("Do you want to overwrite? (y/n) ").lower() == 'y'
        if not overwrite:
            reopen = input("Would you like to open the menu again? (y/n) ")
            if reopen.lower() != "y":
                print("Closing program.")
                exit()
            else:
                return
        else:
            print("Overwriting password.")
    
    password = input("Please enter your password: ")
    passwords[website] = password
    with open("C:/Users/simpl/Projects/password.txt", "w") as file:
        for site, pwd in passwords.items():
            encrypted = fernet.encrypt(pwd.encode()).decode()
            file.write(site + ": " + encrypted + "\n")

    print(website + " : " + password)

def generate_password(min_length, capital= True, numbers=True, special_characters=True):
    #letters = string.ascii_letters
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = string.punctuation

    characters = lowercase
    if capital:
        characters += uppercase
    if numbers:
        characters += digits
    if special_characters:
        characters += special

    password = ""
    meets_criteria = False
    has_capital = False
    has_number = False
    has_special = False

    while not meets_criteria or len(password) < min_length:
        new_char = random.choice(characters)
        password += new_char

        if new_char in uppercase:
            has_capital = True
        elif new_char in digits:
            has_number = True
        elif new_char in special:
            has_special = True

        meets_criteria = True
        if capital:
            meets_criteria = has_capital
        if numbers:
            meets_criteria = has_number
        if special_characters:
            meets_criteria = meets_criteria and has_special

    return password
    #print(letters, digits, special)
def gen():
    website = input("\nWhat website is this password for? ")
    if website in passwords:
        print("Password for " + website + " already exists: " + passwords[website])
        overwrite = input("Do you want to overwrite? (y/n) ").lower() == 'y'
        if not overwrite:
            reopen = input("Would you like to open the menu again? (y/n) ")
            if reopen.lower() != "y":
                print("Closing program.")
                exit()
            else:
                return  # Go back to menu
        else:
            print("Overwriting password.")

    while True:
        try:
            min_length = int(input("Enter minimum password length: "))
            break
        except ValueError:
            print("Invalid input. Only numbers are allowed please try again.\n")

    has_capital = input("Do you want capital letters? (y/n) ").lower() == 'y'
    has_number = input("Do you want to have numbers? (y/n) ").lower() == 'y'
    has_special = input("Do you want to have special characters? (y/n) ").lower() == 'y'
    
    password = generate_password(min_length, has_capital, has_number, has_special)
    passwords[website] = password

    with open("C:/Users/simpl/Projects/password.txt", "w") as file:
        for site, pwd in passwords.items():
            encrypted = fernet.encrypt(pwd.encode()).decode()
            file.write(site + ": " + encrypted + "\n")
    
    print(website + " password saved to password.txt")
    print("The generated password for " + website + " is: " + password)
def menu():
    while True:
        menu = int(input("\nMenu: \n 1. Add Password \n 2. Generate Password \n 3. View Passwords \n 4. Delete Password \n 5. Exit Program \n"))
        if menu == 1:
            add_password()
        elif menu == 2:
            print("Generating Password.")
            gen()
        elif menu == 3:
            attempts = 3
            while attempts > 0:
                masterPassword = input("\nPlease enter the master password: ")
                if masterPassword == MASTER_PASSWORD:
                    attempts = 3
                    print("Login Successful!")
                    with open("C:/Users/simpl/Projects/password.txt", "r") as file:
                        print("\nSaved passwords: ")
                        for line in file:
                            if ":" in line:
                                #print(line.strip())
                                site, encrypted = line.strip().split(":", 1)
                                decrypted = fernet.decrypt(encrypted.encode()).decode()
                                print(site + " : " + decrypted)
                        print(" ")
                        break
                else:
                    attempts -= 1
                    if attempts == 0:
                        print("Too many incorrect attempts. Exiting program.")
                        exit()
                    elif attempts == 1:
                        print("You have " + str(attempts) + " attempt remaining try again.")
                    else:
                        print("You have " + str(attempts) + " attempts remaining try again.")
            reopen = input("Would you like to open the menu again? (y/n) ")
            if reopen.lower() != "y":
                print("Closing program.")
                exit()
        elif menu == 4:
            delete()
        elif menu == 5:
            print("Exiting program.")
            exit()
        else:
            print("Error, please try again.")
def delete():
    print("\nWebsites in the file: ")
    with open("C:/Users/simpl/Projects/password.txt", "r") as file:
        for line in file:
            if ":" in line:
                site = line.strip().split(":",1)[0]
                print(site)
    website = input("Enter the website you want to delete from the file: ").strip().lower()

    lowercaseMap = {site.lower(): site for site in passwords}

    if website in lowercaseMap:
        originalSite = lowercaseMap[website]
        confirmation = input("Do you want to delete the information for " + originalSite + "? (y/n) ").lower()
        if confirmation == "y":
            del passwords[originalSite]
            with open("C:/Users/simpl/Projects/password.txt", "w") as file:
                for site, pwd in passwords.items():
                    encrypted = fernet.encrypt(pwd.encode()).decode()
                    file.write(site + ": " + encrypted + "\n")
            print("Information for " + website + " has been deleted.\n")
            print(" ")
            reopen = input("Would you like to open the menu again? (y/n) ")
            if reopen != "y":
                print("Closing program.")
                exit()
        else:
            print("Deletion process stopped.")
            print(" ")
            reopen = input("Would you like to open the menu again? (y/n) ")
            if reopen != "y":
                print("Closing program.")
                exit()
    else:
        print("No password found for " + website + ".")
        reopen = input("Would you like to open the menu again? (y/n) ")
        if reopen != "y":
            print("Closing program.")
            exit()

#main
print("Welcome to the Password Manager / Generator!")
menu()
