from .exceptions import AccountError
from .utils import is_valid_username,is_valid_phone_number
class Account(object) : 

    def account_edit_info(self,email,username=None,phone_number=None,first_name=None,biography=None,external_url=None) : 
        self.session.headers  ['x-csrftoken'] = self.get_cookies["csrftoken"]
        if external_url : 
            raise AccountError("Editing your links is only available on mobile. Visit the Instagram app and edit your profile to change the websites in your bio.")
        if username :
            self.username = username
        is_valid_username(self.username)
        if phone_number : 
            is_valid_phone_number(phone_number)
        data = {
                    'first_name': first_name,
                    'email': email,
                    'username': self.username,
                    'phone_number': phone_number,
                    'biography': biography,
                    'external_url':None,
                    'chaining_enabled': 'on',
                }         
        return self._make_call(method = "POST",
                               endpoint ="web/accounts/edit/",
                               data = data,
                               response_type ="account.edit_info")   