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
        response = self._make_call(endpoint="web/accounts/login/ajax/",data=data,response_type="auth.login") 
        self.get_cookies 
        return response
    
    def get_suspicious_logins(self) : 
        params = {"device_id" : self.device_id} 
        response = self._make_call(endpoint="session/login_activity/",params=params,response_type="auth.get_suspicious_logins")
        return response['suspicious_logins'] if response else False
    
    def trust_suspicious_logins(self) : 
        suspicious_logins = self.get_suspicious_logins()
        self.session.headers = {
            "x-csrftoken":self.csrf_token
        }
        for suspicious_login in suspicious_logins :
            data = {"login_id"  : suspicious_login["id"] }
            response = self._make_call(endpoint="web/session/login_activity/avow_login/",data=data,response_type="auth.trust_suspicious_logins")

                                                   

        

        
        
    