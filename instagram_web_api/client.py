import requests
from requests import Response
import json
from .auth import Login
from .upload import Upload
from .exceptions import *

class Client (Login,Upload): 
    base_api_url  = "https://www.instagram.com/api/v1/"
    def __init__(self,username,password,settings=None,proxies=None,user_agent = None,selenium_bypass=None) : 
        self.username  = username 
        self.password  = password
        self.logged_in = False
        self.base_headers = {
                            "user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                            "x-ig-app-id": "936619743392459"
                              }
        self.session   = requests.Session()
        self.session.headers = self.base_headers
        self.session.verify  = True
        self.selenium_bypass = selenium_bypass
        if settings :
            self.logged_in = True
            self.session = requests.Session()
            self.session.cookies.update(settings)
    
    @property
    def get_cookies(self) : 
        cookies = {}
        for cookie  in self.session.cookies.items() : 
            cookies[cookie[0]] = cookie[1]
        return cookies
    
    def dump_cookies(self) : 
        with open(f'{self.username}.json','w') as file :
            json.dump(self.get_cookies) 

    def _handle_response(self,response : Response, response_type ) : 
        try : 
            json_response : dict =  response.json()
        except Exception as e : 
            raise UnknownError(f"Error {str(e)} in {response_type} ")
        
        if response.status_code == 200 : 
            if response_type == "auth.login" : 
                if json_response.get('authenticated') == False :
                    raise BadPassword("You entred incorrect password.")
            return json_response
                
        elif response.status_code == 403 : 
            if response_type == "auth.login" : 
                raise IncorrectUsername("You entred incorrect username.")
        message = json_response.get("message")
        if message : 
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

            
    def _make_call(self,url=None,endpoint=None,params=None,data=None) :
        if endpoint : 
            url = self.base_api_url+endpoint
        
        if data : 
            return self.session.post(url,
                                     data=data,
                                     allow_redirects=True)





