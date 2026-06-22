import re
import hashlib
import sqlite3

# Create database
conn = sqlite3.connect("database/password_history.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password_hash TEXT
)
""")
conn.commit()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def check_reuse(password):
    password_hash = hash_password(password)

    cursor.execute(
        "SELECT * FROM passwords WHERE password_hash=?",
        (password_hash,)
    )
    return cursor.fetchone()


def save_password(password):
    password_hash = hash_password(password)
    cursor.execute(
        "INSERT INTO passwords(password_hash) VALUES (?)",
        (password_hash,)
    )
    conn.commit()


def analyze_password(password):
    score = 0
    suggestions = []

    # Length
    if len(password) >= 12:
        score += 30
    elif len(password) >= 8:
        score += 15
    else:
        suggestions.append("Use at least 8 characters.")

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 15
    else:
        suggestions.append("Add uppercase letters.")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 15
    else:
        suggestions.append("Add lowercase letters.")

    # Numbers
    if re.search(r"\d", password):
        score += 15
    else:
        suggestions.append("Add numbers.")

    # Special Characters
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 15
    else:
        suggestions.append("Add special characters.")

    # Common Passwords
    try:
        with open("common_passwords.txt", "r") as file:
            common = file.read().splitlines()

        if password.lower() not in common:
            score += 10
        else:
            suggestions.append("Avoid common passwords.")
    except:
        pass

    # Rating
    if score >= 90:
        strength = "Very Strong"
    elif score >= 70:
        strength = "Strong"
    elif score >= 40:
        strength = "Medium"
    else:
        strength = "Weak"

    return score, strength, suggestions


password = input("Enter Password: ")

if check_reuse(password):
    print("⚠ Password has been used before.")
else:
    score, strength, suggestions = analyze_password(password)

    print(f"\nScore: {score}/100")
    print(f"Strength: {strength}")

    if suggestions:
        print("\nSuggestions:")
        for s in suggestions:
            print("-", s)

    save_password(password)
