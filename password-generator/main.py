import secrets
import os
import time
import json
import codecs

sleep_time = 2.5

def refresh(sleep_time=sleep_time):
    time.sleep(sleep_time)
    os.system("cls" if os.name == "nt" else "clear")

class CryptographyMixin():
    """Provides methods for encryption and decryption using ROT13 cipher."""

    def encrypt(self, data):
        encrypted = codecs.encode(data, 'rot_13')
        return encrypted

    def decrypt(self, data):
        decrypted = codecs.decode(data, 'rot_13')
        return decrypted

class PasswordGenerator(CryptographyMixin):
    def __init__(self):
        self.__saved_passwords = {}
        self.__latest_password = None

        # Check if the passwords.json file exists, if not create it
        if not os.path.exists("passwords.json"):
            with open("passwords.json", "w") as file:
                json.dump({}, file)

            # Set file permissions to read/write for the app and read-only for others
            os.chmod("passwords.json", 0o644)
        
    def generate(self):
        """"Generates a random password based on user's desired password length."""

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

        safe_password = self.encrypt(self.__latest_password) # Encrypt the password before saving
        self.__saved_passwords = {site:safe_password}

        with open("passwords.json", "r") as file:
            passwords = json.load(file)
        
        passwords.update(self.__saved_passwords)

        # Write the updated passwords back to the file
        with open("passwords.json", "w") as f:
            json.dump(passwords, f, indent=4)

        print(self.__saved_passwords)
        self.__saved_passwords = {} # reset password dict for security reasons

        refresh()

    def show(self):
        """"Displays all saved passwords from the JSON file."""
        
        if not os.path.exists("passwords.json") or os.stat("passwords.json").st_size == 0:
            print("No passwords saved yet.")
            refresh()
            return

        print("Saved Passwords:")

        # Read the existing passwords from the file
        with open("passwords.json", "r") as file:
            data = json.load(file)
        for site, password in data.items():
            password = self.decrypt(password) # Decrypt the password before displaying
            print(f"  {site}: {password}")
        
        refresh(10)
    
    def run(self):
        """"Runs the main loop of the password generator application, allowing users to generate, save, and view passwords."""

        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print(r"""
            ------------------------------------------------
            |   P 4 _ _ W 0 R D   G 3 N _ R A 7 0 R   v.2  |
            ------------------------------------------------
            
            | > Generate secure tokens                     |
            | > Save Access Keys                           |
            | > Safe, Encypted, Hackerproof                |
            ------------------------------------------------
            """)
            print("1. Generate password")
            print("2. Save password")
            print("3. Show saved passwords")
            print("4. Exit")
            choice = input("Enter your choice (1-4): ")
            os.system("cls" if os.name == "nt" else "clear")
            
            if choice == "1":
                self.generate()
                choice = input("Do you want to save this password? (y/n): ")
                if choice.lower() == "y":
                    self.save()
                else:
                    refresh(1)
            elif choice == "2":
                self.save()
            elif choice == "3":
                self.show()
            elif choice == "4":
                print("Exiting the program. I'll be back!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

app = PasswordGenerator()
app.run()
