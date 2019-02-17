# -*- coding: utf-8 -*-
from .permissions import has_permission,flow
from rest_framework.generics import ListCreateAPIView
from django.views.generic.base import View
from .serializers import YoutubeSourceSerializer
from .models import YoutubeSource, Video
from pytube import YouTube
from django.shortcuts import redirect
from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from django.conf import settings
from .models import CredentialsModel
from django.http import JsonResponse

class YoutubeListView(ListCreateAPIView):
    serializer_class = YoutubeSourceSerializer
    queryset = YoutubeSource.objects.all()

    def list(self,request):
        res = has_permission(request)
        if res == True:
            return super(YoutubeListView,self).list(request)

        return redirect(res)

class Oauth2CallbackView(View):
    def get(self, request, *args, **kwargs):
        
        if not xsrfutil.validate_token(
            settings.SECRET_KEY, request.GET.get('state').encode(), 1):
                return HttpResponseBadRequest()

        credential = flow.step2_exchange(request.GET)
        storage = DjangoORMStorage(CredentialsModel, 'id', 1, 'credential')
        storage.put(credential)
        
        return redirect('list_api')

class DownloadView(View):
    def get(self,request,playlist_id,*args,**kwargs):
        try:
            videos_list = Video.objects.filter(fk_source__name=playlist_id)
        
            if videos_list.count() == 0:
                return JsonResponse({'error': 'playlist not found'}, status=401)

            for video_id in videos_list:
                yt = YouTube("https://www.youtube.com/watch?v=%s" % video_id.name)
                yt.streams.first().download(settings.DOWNLOAD_PATH)
            
            return JsonResponse({'success': 'playlist downloaded in %s directory' % settings.DOWNLOAD_PATH}, status=200)
        
        except Exception as e:
            print e
            return JsonResponse({'error': 'playlist not found'}, status=401)

