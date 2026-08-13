# make_strong.py
# Combines Chapter 5 generator with Chapter 2 checker

from generate import generate_password
# Ensure this matches the exact name of your Chapter 2 file (minus the .py)
from password_checker import check_password 

def generate_perfect_password():
    attempts = 0
    while True:
        attempts += 1
        # Generate a standard complex password candidate
        candidate = generate_password(
            length=12, 
            upper=True, 
            digits=True, 
            symbols=True, 
            no_ambiguous=False
        )
        
        # Unpack both the score and the issues array from Chapter 2
        score, issues = check_password(candidate)
        
        if score == 5:
            print(f"[+] Perfect 5/5 password found after {attempts} attempt(s)!")
            return candidate

if __name__ == "__main__":
    strong_pwd = generate_perfect_password()
    print(f"Generated Password: {strong_pwd}")