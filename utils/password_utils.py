import random
import string
from password_strength import PasswordPolicy 
# Password strength policy
policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=1,
    special=1
)

# Password strength checker
def check_password_strength(password):
    return not policy.test(password)

# Password generator
def generate_password(length=18):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))
