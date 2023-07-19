from .utils import challenge_json,challenge_type
from .exceptions import ChallengeResolverError
import time
from json import JSONDecodeError
from loguru import logger

logger.add("instagram_bot.log",format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {function} | {message}",colorize=False,enqueue=True,mode="w")

class ChallengeResolver:
    
    def challenge_type(self,checkpoint_url) :
        challenge_url = "https://www.instagram.com"+ checkpoint_url
        response = self._make_call(url=challenge_url,
                                   response_type="ChallengeResolver.security_code")
        # Get the url of code posting.
        
        return challenge_type(response.text),response

    def security_code(self,response,click_send=None) : 
        # Get the page of challenge.
        if click_send : 
            json_response = challenge_json(response.text)
            if json_response['forward'] : 
                self.challenge_url = "https://www.instagram.com"+ json_response['forward']
            else : 
                raise ChallengeResolverError('Unable to find forward link of selecting challenge method choice.')
            logger.info(f'choose email choice : 1 ')
            data = {
                "choice" : "1"
            }
            
            response = self._make_call(url=self.challenge_url,
                                    data=data,
                                    response_type="ChallengeResolver.security_code")
            try : 
                response : dict = response.json()
                self.challenge_url = "https://www.instagram.com"+response['navigation']['forward']
            except JSONDecodeError: 
                json_response = challenge_json(response.text)
                if not json_response["forward"] :
                    raise ChallengeResolverError('Unable to find forward link of sending code and the response not in json format.')
                self.challenge_url = "https://www.instagram.com"+json_response["forward"]
                print(self.challenge_url)

        for i in range(3) : 
            ### Trying 3 attempts
            logger.info(f'{i+1} attempts')
            data = {
                'security_code': str(input('Please enter the security code : ')),
            }
            response = self._make_call(url=self.challenge_url,
                                    data=data,
                                    response_type="ChallengeResolver.security_code")
            
            try : 
                response : dict = response.json()
                if response["status"] == "fail" : 
                    raise ChallengeResolverError('Incorrect security code.')
                self.challenge_url = "https://www.instagram.com"+response['challenge']['navigation']['forward']
            except JSONDecodeError as e:  
                json_response = challenge_json(response.text)
                if not json_response["forward"] :
                    challenge_type,response =  self.challenge_type()
                    return True
                self.challenge_url = "https://www.instagram.com"+json_response["forward"]
                print(self.challenge_url)
        
    def confirmation_code(self,response):
        return
    
    def change_password(self,response) : 
        return
    def enter_security_code(self,response) : 
        return
        
        
        

        

        