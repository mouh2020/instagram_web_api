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



def exception_handler(message) : 
    if  "Media type invalid" in message : 
        raise MediaType(message="Media type invalid")
    elif "Sorry, your password was incorrect. Please double-check your password." == message : 
        raise IncorrectUsername("You entred incorrect username.")
    elif "checkpoint_required" in message  : 
        raise CheckpointRequired("You need to login manualy or activate selenium_bypass.")
    elif "login_required" in message : 
        raise LoginRequired("You need to login manualy or activate selenium_bypass.")
    elif "challenge_required" in message : 
        raise ChallengeRequired("You need to resolve challenge or activate selenium_bypass.")
    elif "Transcode not finished yet." in message : 
        raise UploadMedia(str(message))
    elif "Sorry, this media has been deleted" in message : 
        raise DeletedMedia(str(message))
    elif "Unable to post comment." in message : 
        raise CommentDisabled(message)
    elif "you've changed it twice within 14 days." in message :
        raise AccountNameLimit("You can't change your name right now because you've changed it twice within 14 days. You can however remove your name at any time.")
    elif "You need an email or confirmed phone number." in message : 
        raise AccountError('You need an email or confirmed phone number.')
    elif '"errors":[]' in message : 
        raise AccountError('Unknow error when try change account info.')
    