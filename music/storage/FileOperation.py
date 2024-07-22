from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.db import transaction

class SongStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None):
        '''如果未提供location，则默认为settings.MEDIA_ROOT，指定将保存用户上传文件的目录的绝对文件系统路径'''
        if location is None:
            location = settings.MEDIA_ROOT
        super().__init__(location, base_url)

    def get_available_name(self, name, max_length=None):
        '''当保存新文件时，将调用此方法，其目的是返回目标存储系统中可用于使用的文件名。
        在这种情况下，如果已存在具有相同名称的文件，则会删除它，然后返回原始名称'''
        if self.exists(name):
            os.remove(os.path.join(self.location, name))
        return name

    def create_song_dir(self, next_dir,song_name):
        song_dir = os.path.join(next_dir, str(song_name).lower())
        # 创建文件夹存在exist_ok=True,不存在则创建
        os.makedirs(song_dir, exist_ok=True)
        return song_dir

    def save_song(self, song):
        song_dir = self.create_song_dir(settings.MEDIA_ROOT, song.song_singer)
        # 在歌手目录下创建歌曲目录
        # 在 with transaction.atomic() 语句中执行保存操作
        with transaction.atomic():
            try:
                # 保存音频文件
                audio_file = os.path.join(song_dir, f'{song.song_name}-{song.song_singer}.mp3')
                song.song_file =  self._save(audio_file, song.song_file)

                # 保存图片文件
                image_file = os.path.join(song_dir, f'{song.song_name}-{song.song_singer}.jpg')
                song.song_image =  self._save(image_file, song.song_image)

                # 保存歌词文件
                lyrics_file = os.path.join(song_dir, f'{song.song_name}-{song.song_singer}.lrc')
                song.song_lyrics = self._save(lyrics_file, song.song_lyrics)
                # 保存模型实例
                song.save(update_fields=['song_image', 'song_lyrics', 'song_file'])
            except Exception as e:
                transaction.set_rollback(True)
                pass

    def upload_song(self, song):
        # 保存音频文件
        audio_file = os.path.join(settings.MEDIA_ROOT, f'{song.song_name}-{song.song_singer}.mp3')
        song.song_file =  self._save(audio_file, song.song_file)

        # 保存图片文件
        image_file = os.path.join(settings.MEDIA_ROOT, f'{song.song_name}-{song.song_singer}.jpg')
        song.song_image =  self._save(image_file, song.song_image)

        # 保存歌词文件
        lyrics_file = os.path.join(settings.MEDIA_ROOT, f'{song.song_name}-{song.song_singer}.lrc')
        song.song_lyrics = self._save(lyrics_file, song.song_lyrics)
        song.save(update_fields=['song_image', 'song_lyrics', 'song_file'])





