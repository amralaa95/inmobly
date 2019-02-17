from .views import YoutubeListView,Oauth2CallbackView,DownloadView
from django.conf.urls import url

urlpatterns = [
    url(r'api/',YoutubeListView.as_view(),name="list_api"),
    url(r'oauth2callback', Oauth2CallbackView.as_view(),name='oauth2callback'),
    url(r'download/(?P<playlist_id>[-\w]+)/',DownloadView.as_view(),name='download')
]
