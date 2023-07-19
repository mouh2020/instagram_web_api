import requests
from requests import Response
import json
from .utils import generate_csrf_token
from .auth import Login
from .upload import Upload
from .comment import Comment
from .interaction import Interaction
from .account import Account
from .user import User
from json import JSONDecodeError
from .challenge_resolver import ChallengeResolver
from .exceptions import *
from loguru import logger
logger.add("instagram_bot.log",format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {function} | {message}",colorize=False,enqueue=True,mode="w")

class Client (Login,
              Upload,
              Comment,
              Interaction,
              Account,
              User,
              ChallengeResolver,
              ClientError,
              ): 
    base_api_url  = "https://www.instagram.com/api/v1/"

    def __init__(self,username,password,email=None,email_passowrd=None,settings=None,proxies=None,user_agent = None,challenge_resolver=None) : 
        self.username  = username 
        self.password  = password
        self.settings  = settings
        self.challenge_resolver = challenge_resolver
        self.logged_in = False
        self.attempts  = 0
        self.base_headers = {
                            "user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                            "x-ig-app-id": "936619743392459"
                              }
        self.session   = requests.Session()
        self.session.proxies = proxies
        self.session.headers = self.base_headers
        self.session.verify  = True
        if self.settings :
            self.logged_in = True
            self.session.cookies.update(self.settings)
    
    @property
    def get_cookies(self) : 
        cookies = {}
        for cookie  in self.session.cookies.items() : 
            cookies[cookie[0]] = cookie[1]
        self.settings = cookies
        return cookies
    
    @property
    def device_id(self) : 
        if self.get_cookies and self.settings :
            return self.settings.get('ig_did')
        
    @property
    def csrf_token(self) :
        if self.get_cookies and self.settings :
            return self.settings.get('csrftoken')
        return generate_csrf_token()
        
    @property
    def user_agent(self) : 
        if self.get_cookies and self.settings :
            return self.settings.get("user-agent")
    
    def dump_cookies(self) : 
        with open(f'{self.username}.json','w') as file :
            json.dump(self.get_cookies,file) 

    def _handle_response(self,response : Response, response_type :str ) : 
        print(response.text)
        print(response.status_code)
        try : 
            json_response : dict =  response.json()
            return
        except :
            pass 

    def _make_call(self,method="GET",url=None,endpoint=None,params=None,data=None,response_type=None) :
        if endpoint : 
            url = self.base_api_url+endpoint
        if method == "GET" : 
            response = self.session.get(url,
                                        params=params,
                                        data=data)
            return self._handle_response(response=response,
                                         response_type=response_type)
        elif method == "POST" : 
            response = self.session.post(url,
                                        params=params,
                                        data=data)
            return self._handle_response(response=response,
                                         response_type=response_type)
        
