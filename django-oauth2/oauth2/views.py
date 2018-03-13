import requests
import json
from django.conf import settings
from django.shortcuts import redirect
# Create your views here.

PATH  = settings.CALLBACK_PATH

def callback(request):
    if request.GET.get('state').find('google')>-1:
        return GoogleOAuth2().credential(request)
    else:
        return ({"err" : "oauth provide not support"})


class GoogleOAuth2():
    client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
    client_secret = settings.GOOGLE_OAUTH2_CLIENT_SECRET
    scope = "+".join(settings.GOOGLE_OAUTH2_SCOPES)
    response_type = settings.GOOGLE_OAUTH2_RESPONSE_TYPE
    grant_type  = settings.GOOGLE_OATUH2_GRANT_TYPE

    try:
        code_url = settings.GOOGLE_OAUTH2_CODE
    except:
        code_url = "https://accounts.google.com/o/oauth2/v2/auth"
    try:
        token_url = settings.GOOGLE_OATUH2_TOKEN
    except:
        token_url = 'https://www.googleapis.com//oauth2/v4/token'
    try:
        profile_url = settings.GOOGLE_OAUTH2_PROFILE
    except:
        profile_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    try:
        revoke_url = settings.GOOGLE_OAUTH2_REVOKE
    except:
        revoke_url = 'https://accounts.google.com/o/oauth2/revoke'

    def authorize(self, request):
        host = 'http://'+request.META['HTTP_HOST']
        url = "%s?response_type=%s&client_id=%s&scope=%s&state=google"\
            "&access_type=offline&redirect_uri=%s/%s"%\
            (self.code_url, self.response_type, self.client_id, self.scope, host, PATH)
        return redirect(url)

    def credential(self, request):
        if request.GET.get("code"):
            return self.code2token(request, request.GET.get("code"))
        if request.GET.get("token"):
            return self.token2profile(request, request.GET.get("token"))

    def code2token(self, request, code):
        host = 'http://'+request.META['HTTP_HOST']
        data = {'code':code, 'client_id':self.client_id, \
                'client_secret':self.client_secret, \
                'grant_type': self.grant_type, 'redirect_uri': "%s/%s"%(host, PATH)}

        res = requests.post(self.token_url, data=data)
        data = json.loads(res.content.decode())
        return self.token2profile(request, data['access_token'])

    def token2profile(self, request, token):
        data = requests.get(self.profile_url, params={'access_token':token})
        data = json.loads(data.content.decode())
        return data
