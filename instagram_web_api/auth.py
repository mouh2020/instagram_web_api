from datetime import datetime
from .utils import generate_csrf_token
class Login(object) : 
    def login(self) : 
        time = int(datetime.now().timestamp())
        if self.logged_in : 
            return
        data = {
            "enc_password" : f'#PWD_INSTAGRAM_BROWSER:0:{time}:{self.password}' ,
            'username': self.username,
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}',          
            }
        self.session.headers ['x-csrftoken'] = generate_csrf_token()
        response = self._make_call(endpoint="web/accounts/login/ajax/",data=data) 
        response = self._handle_response(response,response_type="auth.login")
        return response
    
        

        
        
    