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