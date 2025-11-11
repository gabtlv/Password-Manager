import random
import string
import os
from cryptography.fernet import Fernet
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style

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
        if overwrite:
            print("Overwriting password.")
        else:
            reopen = input("Would you like to open the menu again? (y/n) ")
            if reopen.lower() != "y":
                print("Closing program.")
                exit()
            else:
                menu()
    try:
        min_length = int(input("Enter minimum password length: "))
    except ValueError:
        print("Invalid input. Only numbers are allowed please try again.\n")
        gen()
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
        menu = int(input("\nMenu: \n 1. Generate Password \n 2. View Passwords \n 3. Delete Password \n 4. Exit Program \n"))
        if menu == 1:
            print("Generating Password.")
            gen()
        elif menu == 2:
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
        elif menu == 3:
            delete()
        elif menu == 4:
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
def buttonGenerate():
    website = websiteVar.get().strip()
    try:
        length = int(lengthVar.get())
    except ValueError:
        resultVar.set("Please enter a valid number for length.")
        return
    
    if not website:
        resultVar.set("Website field cannot be empty.")
        return
    
    # Check for overwrite
    if website in passwords:
        resultVar.set(f"Password for {website} already exists.")
        return

    # Generate password
    new_pass = generate_password(length, capitalVar.get(), numberVar.get(), specialVar.get())
    passwords[website] = new_pass

    # Save encrypted
    with open("C:/Users/simpl/Projects/password.txt", "w") as file:
        for site, pwd in passwords.items():
            encrypted = fernet.encrypt(pwd.encode()).decode()
            file.write(site + ": " + encrypted + "\n")

    resultVar.set(f"Password for {website} saved!\nGenerated: {new_pass}")
#main
#print("Welcome to the Password Manager / Generator!")

def showFrame(frame):
    frame.tkraise()

#window
window = ttk.Window(themename = "journal")
window.title("Password Manager / Generator")
window.geometry("500x450")
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

#style

style = Style()
#style.configure("Custom.TCheckButton", font=("Calibri", 16, "bold"))

# Welcome Frame
welcomeFrame = ttk.Frame(master = window)
welcomeFrame.grid(row=0, column = 0, sticky="nsew")
welcomeLabel = ttk.Label(welcomeFrame, text = "Welcome to the Password Manager / Generator!", font = "Calibri 16 bold")
welcomeButton = ttk.Button(welcomeFrame, text = "Continue", padding = (50,10), command = lambda: showFrame(menuFrame))
welcomeLabel.pack(padx=40, pady=75)
welcomeButton.pack(pady=50)

# Menu Frame
menuFrame = ttk.Frame(window)
menuFrame.grid(row=0, column=0, sticky="nsew")
menuLabel = ttk.Label(menuFrame, text = "Menu", font = "Calibri 16 bold")
menuLabel.pack(pady=40)
buttonGenerate = ttk.Button(menuFrame, text = "Generate Password", padding = (50,10), command = lambda: showFrame(generateFrame))
buttonView = ttk.Button(menuFrame, text = "View Password", padding = (50,10), command = lambda: showFrame(masterFrame))
buttonDelete = ttk.Button(menuFrame, text = "Delete Password", padding = (50,10), command = lambda: showFrame(deleteFrame))
buttonExit = ttk.Button(menuFrame, text = "Exit Program", padding = (50,10), command = lambda: exit())
buttonGenerate.pack(pady=20)
buttonView.pack(pady=20)
buttonDelete.pack(pady=20)
buttonExit.pack(pady=20)

# Generate Frame
generateFrame = ttk.Frame(window)
generateFrame.grid(row=0, column=0, sticky="nsew")
websiteLabel = ttk.Label(generateFrame, text = "What website is this password for?", font = "Calibri 16 bold")
websiteVar = tk.StringVar()
websiteEntry = ttk.Entry(generateFrame, textvariable = websiteVar)
websiteEntry.get()
lengthLabel = ttk.Label(generateFrame, text = "Length of password", font = "Calibri 16 bold")
lengthVar = tk.IntVar()
lengthEntry = ttk.Entry(generateFrame, textvariable = lengthVar)
capitalVar = tk.BooleanVar(value = False)
numberVar = tk.StringVar(value = False)
specialVar = tk.StringVar(value = False)
capitalCheck = ttk.Checkbutton(generateFrame, text="Include Capital Letters?", variable=capitalVar)
numberCheck = ttk.Checkbutton(generateFrame, text="Include Numbers?", variable=numberVar)
specialCheck = ttk.Checkbutton(generateFrame, text="Include Special Characters?", variable=specialVar)
generateButton = ttk.Button(generateFrame, text = "Generate!", command = lambda: buttonGenerate())
resultVar = tk.StringVar()
passwordLabel = ttk.Label(generateFrame, text = "Password:", font = "Calibri 12 bold")
resultLabel = ttk.Label(generateFrame, textvariable=resultVar, font="Calibri 12 italic", wraplength = 400)
websiteLabel.pack(pady=5)
websiteEntry.pack(pady=5)
lengthLabel.pack(pady=5)
lengthEntry.pack(pady=5)
capitalCheck.pack(pady=5)
numberCheck.pack(pady=5)
specialCheck.pack(pady=5)
generateButton.pack(pady=5)
passwordLabel.pack(side = "left", padx = 10)
resultLabel.pack(side = "left")

# Master Frame
masterFrame = ttk.Frame(window)
masterFrame.grid(row=0, column=0, sticky="nsew")
masterLabel = ttk.Label(masterFrame, text = "Enter the master password:", font = "Calibri 16 bold")
masterVar = tk.StringVar()
masterEntry = ttk.Entry(masterFrame, textvariable = masterVar)
masterEntry.get()
masterButton = ttk.Button(masterFrame, text = "Enter", padding = (50,10), command = lambda: showFrame(viewFrame))
masterLabel.grid(row = 0, column =0, sticky="nw", pady = 50, padx = 20)
masterEntry.grid(row = 0, column =0, sticky="ne", pady = 50, padx = 270)
masterButton.grid(row = 0, column =0, sticky="ne", pady = 100, padx = 275)


# View Frame
viewFrame = ttk.Frame(window)
viewFrame.grid(row=0, column=0, sticky="nsew")


# Delete Frame
deleteFrame = ttk.Frame(window)
deleteFrame.grid(row=0, column=0, sticky="nsew")

#run
showFrame(welcomeFrame)
window.mainloop()

