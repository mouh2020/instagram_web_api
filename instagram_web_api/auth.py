from .utils import generate_csrf_token,get_id

class Login(object) : 

    def login(self) : 
        if self.logged_in : 
            return
        data = {
            "enc_password" : f'#PWD_INSTAGRAM_BROWSER:0:{get_id()}:{self.password}' ,
            'username': self.username,
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}',          
            }
        self.session.headers ['x-csrftoken'] = generate_csrf_token()
        return self._make_call(endpoint="web/accounts/login/ajax/",data=data,response_type="auth.login") 
    
    def get_suspicious_logins(self) : 
        self.session.headers ['x-csrftoken'] = self.get_cookies["csrftoken"]
        self.session.headers ["Content-Type"] = "application/x-www-form-urlencoded"
        self.session.headers ["Referer"]      = "https://www.instagram.com/"  
        device_id = self.device_id
        params = {"device_id" : device_id} 
        return self._make_call(endpoint="session/login_activity/",params=params,response_type="auth.login")['suspicious_logins']


        

        
        
    