import requests
from requests import Response
import json
from .auth import Login
from .exceptions import(BadPassword,
                        UnknownError,
                        IncorrectUsername,
                        CheckpointRequired,
                        LoginRequired,
                        ChallengeRequired)
class Client (Login): 
    base_api_url  = "https://www.instagram.com/api/v1/"
    def __init__(self,username,password,settings_path=None,proxies=None,user_agent = None,selenium_bypass=None) : 
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
        if settings_path :
            self.logged_in = True
            with open(settings_path,"r") as file : 
                settings = json.load(file)
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
        
        elif response.status_code == 400 : 
            message = json_response.get("message")
            if message =="checkpoint_required" : 
                raise CheckpointRequired("You need to login manualy or activate selenium_bypass.")
            elif message == "login_required" : 
                if self.selenium_bypass : 
                    ## Resolve challenge with Selenium
                    return True
                raise LoginRequired("You need to login manualy or activate selenium_bypass.")
            elif message == "challenge_required" : 
                if self.selenium_bypass : 
                    return True
                raise ChallengeRequired("You need to resolve challenge or activate selenium_bypass.")
            
    def _make_call(self,endpoint,params=None,data=None) :
        if data : 
            return self.session.post(self.base_api_url+endpoint,
                                     data=data,
                                     timeout=5,
                                     allow_redirects=True)





