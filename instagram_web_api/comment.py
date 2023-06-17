
class Comment : 
    def comment_to_media(self,comment : str , media_id :str) : 
        self.session.headers  ['x-csrftoken'] = self.get_cookies["csrftoken"]
        data = {
            "comment_text" : comment
        }
        return self._make_call(endpoint = f"comments/{media_id}/add/",
                               data=data,
                               response_type= "comment.comment_to_media")
