import re

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def fallback_response():
    return "I'm sorry, I didn't understand that. Could you please clarify?"
