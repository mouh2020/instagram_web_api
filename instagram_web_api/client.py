import requests
from requests import Response
import json
from .auth import Login
from .upload import Upload
from .comment import Comment
from json import JSONDecodeError
from .utils import exception_handler
class Client (Login,
              Upload,
              Comment): 
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

    def _handle_response(self,response : Response, response_type :str ) : 
        print(response.text)
        print(response.status_code)
        if "Oops, an error occurred." in response.text : 
            raise  UnknownError(f"{response.text} while : {response_type.split('.')[0]}")
        try : 
            print(response.text)
            json_response : dict =  response.json()
        except JSONDecodeError as e : 
            raise UnknownError(f"Error {str(e)} in {response_type} ")
        
        if response.status_code == 200 : 
            if response_type == "auth.login" : 
                if json_response.get('authenticated') == False :
                    raise BadPassword("You entred incorrect password.")
            return json_response
        
        message = json_response.get("message")
        if message : 
            exception_handler(message=message)


    def _make_call(self,url=None,endpoint=None,params=None,data=None,response_type=None) :
        if endpoint : 
            url = self.base_api_url+endpoint
        
        if data : 
            response =  self.session.post(url,
                                     data=data,
                                     allow_redirects=True)
            self._handle_response(response=response,
                                  response_type=response_type)





