class Interaction(object) : 

    def like_modia(self,media_id:str,unlike=None) : 
        self.session.headers  ['x-csrftoken'] = self.get_cookies["csrftoken"]
        return self._make_call(endpoint= f"likes/{media_id}/unlike/" if unlike else  f"likes/{media_id}/like/",
                               response_type="interaction.unlike" if unlike else "interaction.like")
    
    def unlike_media(self,media_id:str) : 
        return self.like_modia(media_id=media_id,
                               unlike=True)
