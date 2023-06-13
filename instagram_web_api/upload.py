from .utils import get_id
from PIL import Image
from moviepy.editor import VideoFileClip
import json,time
from .exceptions import VideoDuration
class Upload : 

    def post_video(self,file_path,caption,from_picture=None) : 
        upload_id = get_id()
        self.__build_upload_id_video(file_path=file_path,
                                     upload_id=upload_id)
        
        data = {
                    'source_type': 'library',
                    'caption': str(caption),
                    'upload_id':str(upload_id),
                    'disable_comments': '0',
                    'like_and_view_counts_disabled': '0',
                    'igtv_share_preview_to_feed': '1',
                    'is_unified_video': '1',
                    'video_subtitles_enabled': '0',
                    'clips_share_preview_to_feed': '1',
                    'disable_oa_reuse': 'false',
                }  
        self.session.headers  ['x-csrftoken'] = self.get_cookies["csrftoken"]
        self.session.headers ["Content-Type"] = "application/x-www-form-urlencoded"
        self.session.headers ["Referer"]      = "https://www.instagram.com/"
        time.sleep(2)
        return self._make_call( url  = 'https://www.instagram.com/api/v1/media/configure_to_clips/' ,
                                data = data,
                                response_type="upload.post_video")
        
    
    def __crop_thumbnail(self,thumbnail_path,height,width) : 
        im = Image.open(str(thumbnail_path))
        offset = (height / 1.78) / 2
        center = width / 2
        # Crop the center of the image
        im = im.crop((center - offset, 0, center + offset, height))
        with open(thumbnail_path, "w") as fp:
            im.save(fp)
            im.close()

    def __build_thumbnail(self,video : VideoFileClip , upload_id) : 
        thumbnail_path = str(upload_id)+".jpg" 
        video.save_frame(thumbnail_path,
                         t=(video.duration / 2))
        self.__crop_thumbnail(thumbnail_path,
                              video.size[1],
                              video.size[0])
        

    def __build_upload_id_video(self,file_path:str,upload_id) :
        
        video = VideoFileClip(filename=file_path)
        (width, height), duration = video.size,video.duration
        duration = 90
        if not(3 < duration < 59 ) : 
            raise VideoDuration("The media should be between 3s and 60s")
        thumbnail_path = f'{str(upload_id)}.jpg'
        video.save_frame(thumbnail_path,t=(duration / 2))
        response = self.__build_thumbnail(video,upload_id)
        data = {
            "client-passthrough":"1",
            "is_clips_video":"1",
            "is_sidecar":"0",
            "media_type":2,
            "for_album":False,
            "video_format":"",
            "upload_id":upload_id,
            "upload_media_duration_ms":int(video.duration*100),
            "upload_media_height":str(height),
            "upload_media_width":str(width),
            "video_transform":None}  
        
        self.session.headers = {
                'content-type': 'application/x-www-form-urlencoded',
                "X-Entity-Name" : f"fb_uploader_{upload_id}",
                "Offset": "0",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                "x-entity-length": str(len(open(file_path,"rb").read())),
                'x-instagram-rupload-params': json.dumps(data),
                "x-ig-app-id": "936619743392459"
                                    }  
        self._make_call(url  = f"https://www.instagram.com/rupload_igvideo/fb_uploader_{str(upload_id)}",
                        data=open(file_path,"rb").read(),
                        response_type="upload.__build_upload_id_video")
 
        self.__build_upload_id_picture(media_path=thumbnail_path,
                                       upload_id=upload_id,
                                       video = True)


        


    def post_picture(self,file_path ,caption) : 
        upload_id = get_id()
        self.__build_upload_id_picture(media_path=file_path,
                                       upload_id=upload_id)
        self.session.headers  ['x-csrftoken'] = self.get_cookies["csrftoken"]
        self.session.headers ["Content-Type"] = "application/x-www-form-urlencoded"
        self.session.headers ["Referer"]      = "https://www.instagram.com/"
        data = {
            'source_type': 'library',
            'caption': str(caption),
            'upload_id':upload_id,
            'disable_comments': '0',
            'like_and_view_counts_disabled': '0',
            'igtv_share_preview_to_feed': '1',
            'is_unified_video': '1',
            'video_subtitles_enabled': '0',
            'disable_oa_reuse': 'false',
        }       
        return self._make_call(url  = 'https://www.instagram.com/api/v1/media/configure/' ,
                               data = data,
                               response_type="upload.post_picture")
        

    def __build_upload_id_picture(self,media_path,upload_id,video=None) : 
        
        img = Image.open(media_path)
        (w,h) = img.size
        self.session.headers = {
            "content-type": "image/jpeg",
            "X-Entity-Name" : f"fb_uploader_{upload_id}",
            "Offset": "0",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "x-entity-length": str(len(open(media_path,"rb").read())),
            "X-Instagram-Rupload-Params": f'{{"media_type": {"2" if video else "1"}, "upload_id": {upload_id}, "upload_media_height": {h}, "upload_media_width": {w}}}',
            "x-ig-app-id": "936619743392459"
                                }
        return self._make_call(url  = f"https://www.instagram.com/rupload_igphoto/fb_uploader_{str(upload_id)}" ,
                               data = open(media_path,"rb").read() ,
                               response_type="upload.__build_upload_id_picture")


        
        
        
