class User : 
    def user_infos(self,username) :
        params = {
            "username" : username
        }
        return self._make_call(method = "GET",
                               endpoint ="users/web_profile_info/",
                               params = params,
                               response_type = "user_infos")
    def user_medias(self,username,amount=15) : 
        params = {
            "count" :amount
        }
        self.session.headers ['x-csrftoken'] = self.csrf_token
        return self._make_call(method = "GET",
                               endpoint =f"feed/user/{username}/username/",
                               params = params,
                               response_type = "user_infos")


