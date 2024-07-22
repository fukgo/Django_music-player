from django import forms
from Apps.Song.models import SongModel,SingerModel,UserSongListModel
class SongsForm(forms.ModelForm):
    class Meta:
        model = SongModel
        fields = ['song_name','song_file','song_bio','song_genre','song_image','song_lyrics','song_singer']

class SingerForm(forms.ModelForm):
    class Meta:
        model = SingerModel
        fields = ['name','gender','dob','image','bio']

class SearchForm(forms.Form):
    parameter = forms.CharField(max_length=100, required=False)

class SongListForm(forms.ModelForm):
    class Meta:
        model = UserSongListModel
        fields = ['list_name']


