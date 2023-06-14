from datetime import datetime
from .exceptions import *
import re,phonenumbers

def generate_csrf_token():
    import string,random
    chars = string.digits+string.ascii_lowercase+string.ascii_uppercase
    csrf_token = ''.join(random.choice(chars) for _ in range(32))
    return csrf_token

def get_id() :
    return int(datetime.now().timestamp())

def is_valid_username(username) : 
    pattern = r"^[a-zA-Z0-9_.][a-zA-Z0-9_.]*$"
    if re.match(pattern, username) is None : 
        raise AccountError("Usernames can only use letters, numbers, underscores and periods.")
def is_valid_phone_number(phone_number) : 
    try : 
        parsed_number = phonenumbers.parse(phone_number)
        valid_phone_number = phonenumbers.is_possible_number(parsed_number)
        if not(valid_phone_number) :
            raise AccountError("Looks like your phone number may be incorrect. Please try entering your full number, including the country code.")
    except Exception as e : 
        raise AccountError(str(e))