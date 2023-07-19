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
    
def challenge_json(content)  -> dict : 
    forward = re.search(re.escape('"forward":"') + "(.*?)" + re.escape('"'),
                        content)
    if forward : 
        forward = forward.group(1)
    else : 
        forward = False
    challenge = re.search(re.escape('"challenge_context":"') + "(.*?)" + re.escape('"'),
                        content)
    if challenge : 
        challenge = challenge.group(1)
    else : 
        challenge = False

    challenge_title = re.search(re.escape('"title":"') + "(.*?)" + re.escape('"'),
                        content)
    if challenge_title : 
        challenge_title = challenge_title.group(1)
    else : 
        challenge_title = False
    page_title = re.search(re.escape('"page_title":"') + "(.*?)" + re.escape('"'),
                        content)
    if page_title : 
        page_title = page_title.group(1)
    else : 
        page_title = False
    return {
        "challenge_title":challenge_title,
        "page_title" : page_title,
        'forward' : forward,
        'challenge_context' : challenge
    }

def challenge_type(content:str) : 
    if "Unusual Login".lower() in content.lower()  :
        return "security_code"
    elif "Password".lower() in content.lower() :
        return "change_password"
    elif "Help us confirm you own this account".lower() in content.lower() : 
        return "confirmation_code"
    elif 'Enter Your Security Code' in content.lower() : 
        return "enter_security_code"
    