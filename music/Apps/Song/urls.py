from django.urls import path
from . import views
app_name = 'song'
urlpatterns = [
    path('uploadsongs/', views.UploadSong.as_view(), name='upload_songs'),
    path('uploadsingers/', views.UploadSinger.as_view(), name='upload_singers'),
    path('list/', views.SongList.as_view(), name='list'),
    path('play/<int:song_id>/', views.play_song, name='play_song'),
    path('home/', views.random_list, name='home'),
    path('pagelist/', views.songlist, name='songlist'),
    path('singerlist/', views.singerlist, name='singerlist'),
    path('singersongs/<int:singer_id>/', views.singersongs, name='singersongs'),
    path('search/', views.search_song, name='search'),
    path('singer_detail/<int:singer_id>/', views.singer_detail, name='singer_detail'),
    path('change_song/<int:song_id>/', views.change_song, name='change_song'),
    path('change_singer/<int:singer_id>/', views.change_singer, name='change_singer'),
    path('user_song_list/<int:id>/', views.UserSongList.as_view(), name='user_song_list'),
    path('user_song_list/<int:list_id>/', views.UserSongList.as_view(), name='put_song_list'),
    path('user_song_list/', views.UserSongList.as_view(), name='post_song_list'),
    path('add_song_to_list/', views.AddSongsToListView.as_view(), name='add_song_to_list'),
    path('song_list/<int:id>/', views.get_song_list_special, name='get_song_list_special'),

]

