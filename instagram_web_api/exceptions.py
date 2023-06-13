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
