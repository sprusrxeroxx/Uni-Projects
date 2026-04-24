import secrets
import os
import time
import json

sleep_time = 3
class PasswordGenerator():
    def __init__(self):
        self.__saved_passwords = {}
        self.__latest_password = None

        # Check if the passwords.json file exists, if not create it
        if not os.path.exists('passwords.json'):
            with open('passwords.json', 'w') as file:
                json.dump({}, file)
        
    def generate(self):
        """"Generates a random password based on user input for length."""

        letters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        numbers = list("0123456789")
        symbols = list("!@#$%^*()+_*")
        
        try:
            password_length = int(input("How many characters do you want your password to have: "))
        except ValueError:
            password_length = 12
        
        password_list = []
        
        while(len(password_list) <= password_length):
            
            if password_length == 0:
                print("Error: Please enter a Non-Zero length")
                return
            
            random_letter = secrets.choice(letters)
            password_list.append(random_letter)
        
            random_number = secrets.choice(numbers)
            password_list.append(random_number)
            
            random_symbol = secrets.choice(symbols)
            password_list.append(random_symbol)

            secrets.SystemRandom().shuffle(password_list)

        password = ""
        
        for char in password_list:
            password += char
        
        self.__latest_password = password
        print(f"Your password is: {password}")
        refresh()

    def save(self):
        """"Saves the latest generated password to a JSON file with the site name as the key."""

        site = input("What's the password used for: ")

        if site.strip() == "":
            print("Error: Site name cannot be empty.")
            refresh()
            return

        if self.__latest_password is None:
            print("No password generated yet. Please generate a password before saving.")
            refresh()
            return

        self.__saved_passwords = {site:self.__latest_password}

        with open('passwords.json', 'r') as file:
            passwords = json.load(file)
        
        passwords.update(self.__saved_passwords)

        # Write the updated passwords back to the file
        with open("passwords.json", "w") as f:
            json.dump(passwords, f, indent=4)

        print(self.__saved_passwords)
        refresh()

    def show(self):
        """"Displays all saved passwords from the JSON file."""
        
        if not os.path.exists('passwords.json') or os.stat('passwords.json').st_size == 0:
            print("No passwords saved yet.")
            refresh()
            return

        print("Saved Passwords:")

        # Read the existing passwords from the file
        with open('passwords.json', 'r') as file:
            data = json.load(file)
        for site, password in data.items():
            print(f"  {site}: {password}")
        
        refresh()
    
    def run(self):
        """"Runs the main loop of the password generator application, allowing users to generate, save, and view passwords."""

        while True:
            print(r"""
            ------------------------------------------------
            |   P A S S W O R D   G E N E R A T O R   v.1  |
            ------------------------------------------------
            
            | > Generate secure tokens                     |
            | > Save Access Keys                           |
            | > Safe, Encypted, Easy                       |
            ------------------------------------------------
            """)
            print("1. Generate password")
            print("2. Save password")
            print("3. Show saved passwords")
            print("4. Exit")
            choice = input("Enter your choice (1-4): ")
            os.system('cls' if os.name == 'nt' else 'clear')
            
            if choice == '1':
                self.generate()
                choice = input("Do you want to save this password? (y/n): ")
                if choice.lower() == 'y':
                    self.save()
                else:
                    refresh()
            elif choice == '2':
                self.save()
            elif choice == '3':
                self.show()
            elif choice == '4':
                print("Exiting the program. I'll be back!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

def refresh():
    time.sleep(sleep_time)
    os.system('cls' if os.name == 'nt' else 'clear')

app = PasswordGenerator()
app.run()
