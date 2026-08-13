# generate.py
# Secure password generator

import argparse
import secrets
import string

SYMBOLS = "!@#$%^&*()_+[]{}|;:,.<>?"

def generate_password(length, upper, digits, symbols, no_ambiguous, prefix=""):
    required = []
    
    # Define primary character pools
    upper_pool = string.ascii_uppercase
    digit_pool = string.digits
    symbol_pool = SYMBOLS
    available = string.ascii_lowercase

    # Exercise 14: Filter out ambiguous characters if the flag is True
    if no_ambiguous:
        ambiguous = "0O1lIi"
        upper_pool = "".join([c for c in upper_pool if c not in ambiguous])
        digit_pool = "".join([c for c in digit_pool if c not in ambiguous])
        symbol_pool = "".join([c for c in symbol_pool if c not in ambiguous])
        available = "".join([c for c in available if c not in ambiguous])

    if upper:
        required.append(secrets.choice(upper_pool))
        available += upper_pool

    if digits:
        required.append(secrets.choice(digit_pool))
        available += digit_pool

    if symbols:
        required.append(secrets.choice(symbol_pool))
        available += symbol_pool

    # Exercise 16: Adjust target length to account for the prefix
    prefix_length = len(prefix)
    random_length_needed = length - prefix_length

    if random_length_needed < len(required):
        raise ValueError("Length is too short to fulfill requirements with that prefix.")

    chars = required.copy()
    while len(chars) < random_length_needed:
        chars.append(secrets.choice(available))

    # Shuffle only the randomly generated characters
    secrets.SystemRandom().shuffle(chars)
    
    # Exercise 16: Prepend the prefix securely to the final string
    return prefix + "".join(chars)

def main():
    parser = argparse.ArgumentParser(
        description = "Secret password generator"
    )
    parser.add_argument("-l", "--length", type = int, default = 12)
    parser.add_argument("-c", "--count", type = int, default = 1)
    parser.add_argument("--upper", action = "store_true")
    parser.add_argument("--digits", action = "store_true")
    parser.add_argument("--symbols", action = "store_true")
    
    # Exercise 14 & 16: Added new command-line flags
    parser.add_argument("--no-ambiguous", action = "store_true", help = "Remove visually similar characters")
    parser.add_argument("--prefix", type = str, default = "", help = "Static prefix for the password")
    
    parser.add_argument("--save", help = "Save passwords to a text file")
    args = parser.parse_args()

    passwords = []
    for _ in range(args.count):
        passwords.append(
            generate_password(
                args.length,
                args.upper,
                args.digits,
                args.symbols,
                args.no_ambiguous,
                args.prefix
            )
        )

    for password in passwords:
        print(password)

    if args.save:
        with open(args.save, "w") as file:
            for password in passwords:
                file.write(password + "\n")
        print("Passwords saved.")

if __name__ == "__main__":
    main()