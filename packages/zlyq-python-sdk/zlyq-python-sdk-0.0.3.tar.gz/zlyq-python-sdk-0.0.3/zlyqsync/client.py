from dataclasses import dataclass, asdict
import requests
import json
import os, sys
from requests_toolbelt.multipart.encoder import MultipartEncoder

sys.path.append("..")
from zlyqauth import sign as signAuth, appToken as appTokenAuth

@dataclass
class SyncClient():
    appKey:str
    appSecret:str
    appId:int
    address:int

    def __buildHeader(self, params):
        header = {}
        sign, urlParam = signAuth.addSign(params, self.appId, self.appSecret)
        appToken = appTokenAuth.addAppToken(self.appKey, self.appSecret)
        header['Content-Type'] = 'application/json'
        header['X-Sign'] = sign
        header['X-App-Token'] = appToken

        return header, urlParam

    def __httpPost(self, address, apiUrl, params, body):
        params = params if params else {}
        header, urlParams = self.__buildHeader(params)
        urlStr = address + apiUrl + "?" + urlParams

        datas = json.dumps(body)
        resp = requests.post(urlStr, data=datas, headers=header)

        return resp.text

    def __httpMultiForm(self, address, apiUrl, params, body):
        params = params if params else {}
        header, urlParams = self.__buildHeader(params)
        urlStr = address + apiUrl + "?" + urlParams

        multipart_encoder = MultipartEncoder(
            fields=body,
        )
        header['Content-Type'] = multipart_encoder.content_type
        resp = requests.post(
            urlStr,
            data=multipart_encoder,
            headers=header)

        return resp.text

    def userInfoSynchronize(self, userInfo):
        body = asdict(userInfo)
        return self.__httpPost(self.address, "/api/v1/synchronize/userInfo", None, body)

    def historySynchronize(self, trackInfo):
        body = asdict(trackInfo)
        return self.__httpPost(self.address, "/trace", None, body)

    def videoUpload(self, video):
        body = {
            "image": ('imageFile', video.image, 'application/octet-stream'),
            "video": ('videoFile', video.video, 'application/octet-stream'),
            "title": video.title,
            "userId": video.userId,
            "content": video.content,
            "orgFileName": video.orgFileName,
            "os": str(video.os),
            "source": str(video.source),
            "thirdId": video.thirdId,
            "thirdExtra": video.thirdExtra,
        }
        return self.__httpMultiForm(self.address, "/api/v1/videoUploadSync", None, body)

    def videoSynchronize(self, video):
        body = asdict(video)
        return self.__httpPost(self.address, "/api/v1/videoSync", None, body)

    def imageUpload(self, image):
        body = {
            "image": ('file', image.image, 'application/octet-stream'),
            "description": image.description,
            "userId": image.userId,
            "source": str(image.source),
            "thirdId": image.thirdId,
            "thirdExtra": image.thirdExtra,
        }
        return self.__httpMultiForm(self.address, "/api/v1/imageUploadSync", None, body)

    def articleSynchronize(self, article):
        body = asdict(article)
        return self.__httpPost(self.address, "/api/v1/articleSync", None, body)

    def articleUpload(self, article):
        body = asdict(article)
        return self.__httpPost(self.address, "/api/v1/articleUploadSync", None, body)

    def mediaLikeSynchronize(self, mls):
        body = asdict(mls)
        return self.__httpPost(self.address, "/api/v1/mediaLikeSync", None, body)

    def mediaFavoriteSynchronize(self, mfs):
        body = asdict(mfs)
        return self.__httpPost(self.address, "/api/v1/mediaFavoriteSync", None, body)

    def commentSynchronize(self, comments):
        body = asdict(comments)
        return self.__httpPost(self.address, "/api/v1/commentSync", None, body)

    def commentLikeSynchronize(self, cls):
        body = asdict(cls)
        return self.__httpPost(self.address, "/api/v1/commentLikeSync", None, body)
