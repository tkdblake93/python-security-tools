# Step 1: The Function Skeleton
def check_password(password):
    score = 0 # starts at 0, increases for each rule passed
    issues = [] # collects every problem found
    common_words = ["password", "letmein", "qwerty", "admin", "welcome", "monkey"]

    # Step 2: Length Check
    if len(password) >= 8:
        score += 1
    else:
        issues.append("Password is too short. Use at least 8 characters.")

    # Step 3: Uppercase Check
    has_upper = any(c.isupper() for c in password)
    if has_upper:
        score += 1
    else:
        issues.append("No uppercase letters found. Add at least one capital letter.")

    # Step 4: Digit Check
    has_digit = any(c.isdigit() for c in password)
    if has_digit:
        score += 1
    else:
        issues.append("No numbers found. Add at least one digit.")

    # Step 5: Special Character Check
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    has_special = any(c in special_chars for c in password)
    if has_special:
        score += 1
    else:
        issues.append("No special characters found. Try !@#$ or %.")

    # Exercise: Detect and penalize common words
    is_common = False
    for common_word in common_words:
        if common_word in password.lower():
            is_common = True
            break

    if is_common:
        score = 0
        issues.append("Contains a common word (like 'admin' or 'password'). Please be more creative.")

    # Step 6: Length Bonus
    if len(password) >= 12:
        score += 1 # maximum score is 5
    return score, issues

# Step 7: Verdict Function
def get_verdict(score):
    if score <= 1:      return "VERY WEAK"
    elif score == 2:    return "WEAK"
    elif score == 3:    return "FAIR"
    elif score == 4:    return "STRONG"
    else:               return "VERY STRONG"

# Step 8: Print the Results
def print_results(score, issues):
    verdict = get_verdict(score)
    print(f"Score: {score} / 5")
    print(f"Verdict: {verdict}")
    print()
    if issues:
        print("Issues found:")
        for issue in issues:
            print(f" - {issue}")
        print()
    else:
        print("Excellent password. No issues found.")
        print()

# Safely tucked away so it only triggers when running this file directly!
if __name__ == "__main__":
    print("=" * 40)
    print("Password Strength Checker")
    print("=" * 40)
    print("Type 'quit' to exit.\n")
    while True:
        print()
        password = input("Enter a password: ")
        if password.lower() == "quit":
            print("Goodbye.")
            break
        score, issues = check_password(password)
        print_results(score, issues)
