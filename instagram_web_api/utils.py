from datetime import datetime
from .exceptions import *

def generate_csrf_token():
    import string,random
    chars = string.digits+string.ascii_lowercase+string.ascii_uppercase
    csrf_token = ''.join(random.choice(chars) for _ in range(32))
    return csrf_token

def get_id() :
    return int(datetime.now().timestamp())

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
