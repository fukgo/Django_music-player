from rest_framework import serializers
from .models import SongModel, UserSongListModel

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongModel
        fields = ['song_name', 'song_singer','id']

