import secrets
import os
import time
import json

sleep_time = 3
class PasswordGenerator():
    def __init__(self):
        self.__saved_passwords = {}
        self.__latest_password = None
        
    def generate(self):
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
            data = json.load(file)
        
        data.update(self.__saved_passwords)

        with open("passwords.json", "w") as f:
            json.dump(data, f, indent=4)

        print(self.__saved_passwords)
        refresh()

    def show(self):
        if not os.path.exists('passwords.json') or os.stat('passwords.json').st_size == 0:
            print("No passwords saved yet.")
            refresh()
            return

        print("Saved Passwords:")

        with open('passwords.json', 'r') as file:
            data = json.load(file)
        for site, password in data.items():
            print(f"  {site}: {password}")
        
        refresh()
    
    def run(self):
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
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

def refresh():
    time.sleep(sleep_time)
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    app = PasswordGenerator()
    app.run()
