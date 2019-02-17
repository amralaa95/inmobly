# -*- coding: utf-8 -*-
from .permissions import get_authenticated_service
from googleapiclient.discovery import build
from django.core.files import File
import requests
import tempfile

def create_videos_list(source):
    try:
        service = get_authenticated_service()
        
        if source.type == 1:
            playlist_id = get_user_playlist_id(service,source.name)
        else:
            playlist_id = source.name     

        get_playlist_videos(service,playlist_id,source)
    except Exception as e:
        print e

def get_user_playlist_id(service_client,user):
    args = {'part':'contentDetails',
            'forUsername':user}
    playlist_id = service_client.channels().list(**args).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return playlist_id

def get_playlist_videos(service_client,playlist_id,source,next_page=False):
    videos = []
    args = {'part':'contentDetails',
            'maxResults':50,
            'playlistId':playlist_id}
    if next_page:
        args['pageToken'] = next_page

    playlist_videos= service_client.playlistItems().list(**args).execute()
    next_page = playlist_videos.get('nextPageToken', False)
    playlist_videos = playlist_videos.get('items',[])
    
    for curr_video in playlist_videos:
        videos.append(curr_video['contentDetails']['videoId'])
    
    save_videos_info (service_client,videos,source)
    if next_page:
        get_playlist_videos(service_client,playlist_id,source,next_page)
    
    return

def save_videos_info(service_client,videos,source):
    from .models import Video
    args = {'part': 'snippet,contentDetails,statistics',
            'maxResults': 50,
            'id': ','.join(videos)}
    videos_list = []
    videos_info = service_client.videos().list(**args).execute()

    for curr_video in videos_info.get('items',[]):
        thumbnail = curr_video['snippet']['thumbnails']['default']['url']
        image = curr_video['snippet']['thumbnails']['high']['url']
        try:
            curr_v = Video(fk_source = source, name=curr_video['id'], title = unicode(curr_video['snippet']['title']), 
                        duration = curr_video['contentDetails']['duration'], views = curr_video['statistics']['viewCount'], 
                        thumbnail_url = thumbnail, original_url = image)
            curr_v = image_path(curr_v,'hq')
            curr_v = image_path(curr_v,'default')
            videos_list.append(curr_v)
        except Exception as e: 
            '''
             exception will be in old videos in curr_video['statistics']['viewCount'], KeyError: 'viewCount'
            '''
            print e

    Video.objects.bulk_create(videos_list)


def image_path(instance, type):
    if type == 'hq':
        image_url = instance.original_url
    else:
        image_url = instance.thumbnail_url

    request = requests.get(image_url, stream=True)
    if request.status_code != requests.codes.ok:
        return    
    name = instance.name    
    new_filename = "%s-%s" % (name, type)
    tmp_file = tempfile.NamedTemporaryFile()

    for block in request.iter_content(1024 * 8):
        if not block:
            break
        tmp_file.write(block)

    if type == 'hq':
        instance.original_image = File(tmp_file,new_filename)
    else:
        instance.thumbnail_image = File(tmp_file,new_filename)

    return instance