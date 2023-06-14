class ClientError(Exception) : 
    def __init__(self,message) : 
        self.message = message

class LoginRequired(ClientError) : 
    "raise when login is required"
    pass
class ChallengeRequired(ClientError) : 
    "raise when login is required"
    pass
class UnknownError(ClientError) : 
    "raise when login is required"
    pass
class BadPassword(ClientError) : 
    "raise when password is incorrect"
    pass
class IncorrectUsername(ClientError) : 
    "raise when password is incorrect"
    pass
class CheckpointRequired(ClientError) : 
    "raise when login is required"
    pass
class VideoDuration(ClientError) : 
    "raise when video duration more than 30s or less than 3s "
    pass
class MediaType(ClientError) : 
    "raise when the media type is invalid "
    pass
class UploadMedia(ClientError) : 
    "raise when the media not properly uploaded "
    pass
class DeletedMedia(ClientError) : 
    "raise when the media not found "
    pass
class CommentDisabled(ClientError) : 
    "raise when the media not found "
    pass
class AccountNameLimit(ClientError): 
    "raise when try change name twice within 14 days."
    pass
class AccountError(ClientError): 
    "raise when try change name twice within 14 days."
    pass   

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