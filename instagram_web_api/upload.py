from .utils import get_id
from PIL import Image
class Upload : 
    upload_id = get_id()
    def post_picture(self,file_path ,caption) : 
        self.__build_upload_id_photo(media_path=file_path)
        self.session.headers  ['x-csrftoken'] = self.get_cookies["csrftoken"]
        self.session.headers ["Content-Type"] = "application/x-www-form-urlencoded"
        self.session.headers ["Referer"]      = "https://www.instagram.com/"
        data = {
            'source_type': 'library',
            'caption': str(caption),
            'upload_id': self.upload_id,
            'disable_comments': '0',
            'like_and_view_counts_disabled': '0',
            'igtv_share_preview_to_feed': '1',
            'is_unified_video': '1',
            'video_subtitles_enabled': '0',
            'disable_oa_reuse': 'false',
        }       
        response = self._make_call(url  = 'https://www.instagram.com/api/v1/media/configure/' ,
                               data = data)
        self._handle_response(response,response_type="upload.post_picture")

    def __build_upload_id_photo(self,media_path) : 
        
        img = Image.open(media_path)
        (w,h) = img.size
        self.session.headers = {
            "content-type": "image/jpeg",
            "X-Entity-Name" : f"fb_uploader_{self.upload_id}",
            "Offset": "0",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "x-entity-length": str(len(open(media_path,"rb").read())),
            "X-Instagram-Rupload-Params": f'{{"media_type": 1, "upload_id": {self.upload_id}, "upload_media_height": {h}, "upload_media_width": {w}}}',
            "x-ig-app-id": "936619743392459"
                                }
        response = self._make_call(url  = f"https://www.instagram.com/rupload_igphoto/fb_uploader_{str(self.upload_id)}" ,
                               data = open(media_path,"rb").read() )
        self._handle_response(response,response_type="upload.__build_upload_id_photo")


        
        
        
