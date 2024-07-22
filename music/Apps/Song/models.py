from django.db import models
from Apps.User.models import CustomUser
from django.dispatch import receiver
gender_choices = [('0', '女'), ('1', '男')]
from django.db.models.signals import post_save
class SingerModel(models.Model):
    class Meta:
        db_table = 'singer_model'
    name = models.CharField(max_length=100,unique=True,verbose_name='歌手姓名')
    gender = models.CharField(max_length=5,choices=gender_choices,verbose_name='性别')
    dob = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='Song/singers/Img',blank=True, null=True)
    #个人简历
    bio = models.TextField(blank=True, null=True,default='暂无简介')

    def __str__(self):
        return self.name

    def gender_display(self):
        return self.get_gender_display()

class SongModel(models.Model):
    class Meta:
        db_table = 'song_model'
    song_name = models.CharField(max_length=100,verbose_name='歌曲名称',unique=True)
    song_singer = models.ForeignKey(SingerModel, on_delete=models.CASCADE, related_name="songs", verbose_name='歌手')
    #指代的是self.name
    song_genre = models.CharField(max_length=100,verbose_name='歌曲风格')
    #release_date = models.DateField()
    song_file = models.FileField(verbose_name='歌曲文件',upload_to='Song/songs/Files')
    song_image = models.FileField(verbose_name='歌曲图片', upload_to='Song/songs/Imgs')
    song_lyrics = models.FileField(verbose_name='歌词文件',upload_to='Song/songs/Lyrics')
    song_bio = models.TextField(verbose_name='歌曲简介')
    #song_singer = models.ForeignKey(Singer,on_delete=models.CASCADE)


    def __str__(self):
        return self.song_name


class UserSongListModel(models.Model):
    class Meta:
        db_table = 'user_song_list'
    list_name = models.CharField(max_length=100,verbose_name='歌曲列表名称')
    song = models.ManyToManyField(SongModel, related_name='belong_list')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='my_song_list')

    def __str__(self):
        return self.user.username + '的歌手列表' + self.list_name

