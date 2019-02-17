from rest_framework import serializers
from .models import YoutubeSource

class YoutubeSourceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = YoutubeSource
        fields = '__all__'
