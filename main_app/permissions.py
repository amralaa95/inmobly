from oauth2client.client import  OAuth2WebServerFlow
from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from django.conf import settings
from googleapiclient.discovery import build
from django.contrib.auth.models import User


flow = OAuth2WebServerFlow(
    client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
    client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
    scope='https://www.googleapis.com/auth/youtube',
    redirect_uri='http://localhost:8000/oauth2callback')

def get_authenticated_service():
    from .models import CredentialsModel
    
    storage = DjangoORMStorage(CredentialsModel, 'id', 1, 'credential')
    credentials = storage.get()
    client = build('youtube', 'v3', credentials=credentials)
    
    return client


def has_permission( request):
    from .models import CredentialsModel

    storage = DjangoORMStorage(CredentialsModel, 'id', 1, 'credential')
    credential = storage.get()

    if credential is None or credential.invalid == True:
        flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, 1)
        authorize_url = flow.step1_get_authorize_url()
        return authorize_url

    return True

   
