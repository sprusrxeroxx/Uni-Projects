import random

class PasswordGenerator():
    
    def _init_(self):
        self.saved_passwords = {}
        self.__latest_password = null
        
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
            
            random_letter = random.choice(letters)
            password_list.append(random_letter)
        
            random_number = random.choice(numbers)
            password_list.append(random_number)
            
            random_symbol = random.choice(symbols)
            password_list.append(random_symbol)
            
        random.shuffle(password_list)
        password = ""
        
        for char in password_list:
            password += char
        
        self.__latest_password = password
        print(f"Your password is: {password}")
    
    def save(self):
        site = input("What's the password used for: ")
        #self.saved_passwords[site] = self.__latest_password
        print(self.saved_passwords)
    
    def show(self):
        pass
    
    def run(self):
       while True:
        print(r"""
        ------------------------------------------------
        |   P A S S W O R D   G E N E R A T O R   v.1      |
        ------------------------------------------------
        
        | > Generate secure tokens                         |
        | > Save Access Keys                               |
        | > Safe, Encypted, Easy                           |
        ------------------------------------------------
        """)
        print("1. Generate password")
        print("2. Save password")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")
        print("\n")
        
        if choice == '1':
            self.generate()
        elif choice == '2':
            self.save()
        elif choice == '3':
            self.show()
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
    
#if __name__ == "__main__":
   # app = PasswordGenerator()
    #app.run()
app = PasswordGenerator()

app.generate()
app.save()
