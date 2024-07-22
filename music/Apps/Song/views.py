import urllib.parse
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.views import View
from django.contrib import messages
import os
import random
from django.conf import settings
from .forms import SongsForm,SingerForm,SongListForm
import urllib.parse
from .serializers import SongSerializer
from django.shortcuts import render
from Apps.User.models import CustomUser
from .models import SongModel, SingerModel, UserSongListModel
def return_background_img():
    # 定义图片文件夹的路径
    image_dir = os.path.join(settings.STATICFILES_DIRS[0], 'music/images/background')
    # 获取文件夹中所有图片的文件名
    images = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    # 从列表中随机选择一个图片
    random_image = random.choice(images)
    # 返回图片的路径
    image_path = os.path.join('music/images/background', random_image)
    # 将路径中的反斜杠替换为正斜杠
    web_friendly_path = image_path.replace('\\', '/')
    print(web_friendly_path)
    return web_friendly_path

def play_song(request,song_id):
    song = SongModel.objects.get(id=song_id)
    back_img = return_background_img()
    song_file_url = urllib.parse.unquote(song.song_file.url)
    song_image_url = urllib.parse.unquote(song.song_image.url)
    song_lyrics_url = urllib.parse.unquote(song.song_lyrics.url)
    count = SongModel.objects.count()
    return render(request, 'Song/player.html', {'song': song, 'background_img': back_img, 'song_file_url': song_file_url, 'song_image_url': song_image_url, 'song_lyrics_url': song_lyrics_url, 'count': count})
def songlist(request):
    songs = SongModel.objects.all()
    return render(request, 'Song/songs_list.html', {'songs': songs})

def singerlist(request):
    singers = SingerModel.objects.all()
    return render(request, 'Song/singer_list.html', {'singers': singers})


def random_list(request):
    songs = SongModel.objects.all()
    count = SongModel.objects.count()
    if count>=3:
        random_songs = SongModel.objects.order_by('?')[:3]
    else:
        random_songs = SongModel.objects.all()
    return render(request, 'Song/home.html', {'random_songs': random_songs, 'songs': songs})
def singersongs(request,singer_id):
    singer = SingerModel.objects.get(id=singer_id)
    songs = singer.songs.all()
    return render(request, 'Song/singersongs.html', {'songs': songs, 'singer': singer})

def singer_detail(request, singer_id):
    singer = SingerModel.objects.get(id=singer_id)
    return render(request, 'Song/singer/singer_detail.html', {'singer': singer})

def search_song(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        songs = SongModel.objects.filter(Q(song_name__contains=keyword) | Q(song_singer__name__contains=keyword))
        return render(request, 'Song/search_list.html', {'songs': songs, 'keyword': keyword})
    else:
        return render(request, 'Song/search_list.html')

def change_song(request, song_id):
    song = SongModel.objects.get(id=song_id)
    if request.method == 'POST':
        form = SongsForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            song = form.save()
            messages.success(request, '修改成功')
            return render(request, 'Song/change_song.html', {'form': form})
        else:
            return render(request, 'Song/change_song.html', {'form': form})
    else:
        form = SongsForm(instance=song)
        return render(request, 'Song/change_song.html', {'form': form})

def change_singer(request, singer_id):
    singer = SingerModel.objects.get(id=singer_id)
    if request.method == 'POST':
        form = SingerForm(request.POST, request.FILES, instance=singer)
        if form.is_valid():
            singer = form.save()
            messages.success(request, '修改成功')
            return render(request, 'Song/change_singer.html', {'form': form,'singer':singer})
        else:
            return render(request, 'Song/change_singer.html', {'form': form,'singer':singer})
    else:
        form = SingerForm(instance=singer)
        return render(request, 'Song/change_singer.html', {'form': form,'singer':singer})
class SongList(APIView):
    def get(self, request, format=None):
        songs = SongModel.objects.all()
        serializer = SongSerializer(songs, many=True)
        print(serializer.data)
        return Response(serializer.data)
class UploadSong(View):
    form = SongsForm
    template_name = 'Song/uploadsongs.html'
    def get(self, request, *args, **kwargs):
        songs = SongModel.objects.all()
        return render(request, self.template_name, {'songs': songs,'singers':SingerModel.objects.all()})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            song = form.save()
            messages.success(request, '歌曲添加成功')
            return render(request, self.template_name, {'form': form,'singers':SingerModel.objects.all()})
        else:
            print(form.errors)
            return render(request, self.template_name, {'form': form,'singers':SingerModel.objects.all()})
class UploadSinger(View):
    form = SingerForm
    template_name = 'Song/uploadsingers.html'

    def get(self, request, *args, **kwargs):
        singers = SingerModel.objects.all()
        return render(request, self.template_name, {'singers': singers})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        print(form.data.get('gender'))
        if form.is_valid():
            singer = form.save()
            messages.success(request, '歌手添加成功')
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})


class UserSongList(View):
    form = SongListForm
    template_name = 'Song/personal/song_list.html'
    def get(self, request, id):
        user = CustomUser.objects.get(id=id)
        song_lists = user.my_song_list.all()
        all_songs = SongModel.objects.all()
        return render(request, self.template_name, {'song_lists': song_lists,'all_songs':all_songs})

    def post(self, request, list_id=None):
        if list_id:
            song_list = UserSongListModel.objects.get(id=list_id)
            form = self.form(request.POST, instance=song_list)
            if form.is_valid():
                song_list = form.save(commit=False)
                song_list.user = request.user
                song_list.save()
                return HttpResponse('success')
        form = self.form(request.POST)
        if form.is_valid():
            song_list = form.save(commit=False)
            song_list.user = request.user
            song_list.save()
            return HttpResponse('success')
        else:
            print(form.errors)
            return render(request, self.template_name, {'form': form})

    def delete(self, request, *args, **kwargs):
        id = self.kwargs.get('song_list_id')
        if id:
            song_list = UserSongListModel.objects.get(id=id)
            song_list.delete()
            return HttpResponse('success')
def get_song_list_special(request, id):
    list = UserSongListModel.objects.get(id=id)
    songs = list.song
    return render(request, 'Song/personal/get_song_list.html', {'songs': songs,'list':list})


class AddSongsToListView(View):
    def post(self, request, *args, **kwargs):
        print(request.POST)
        song_ids = request.POST.getlist('song_ids')
        song_list_id = request.POST.get('list_id')
        if song_list_id is not None:
            try:
                song_list = UserSongListModel.objects.get(id=song_list_id)
                for song_id in song_ids:
                    song = SongModel.objects.get(id=song_id)
                    song_list.song.add(song)
                print(song_list.song.all())
                return JsonResponse({'status': 'success'})
            except UserSongListModel.DoesNotExist:
                print('Song list does not exist')
                # Handle the case where the song_list does not exist
                return JsonResponse({'status': 'error', 'message': 'Song list does not exist'})
        else:
            print('Song list id not provided')
            return JsonResponse({'status': 'error', 'message': 'Song list id not provided'})