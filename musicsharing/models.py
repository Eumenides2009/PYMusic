from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
def validate_music_file(file):
	import os
	ext = os.path.splitext(file.name)[1]
	valid_extensions = ['.mp3','.flac']

	if not ext in valid_extensions:
		raise ValidationError(u'Unsupported file extension.')

class Music(models.Model):
	name = models.CharField(max_length=160,primary_key=True)
	artist = models.CharField(max_length=160,null=True)
	album = models.CharField(max_length=160,null=True)
	content = models.FileField(upload_to='music',validators=[validate_music_file])
	picture = models.ImageField(upload_to='music_image',default='music_image/default.jpg')
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	lyric = models.FileField(upload_to='music_lyric',null=True)


	def __unicode__(self):
		return self.name


class Profile(models.Model):
	gender_choice = (
		('M','Male'),
		('F','Female'),
		('G','Gay'),
		('L','Lesbian'),
		('B','Bisexual'),
		('T','transgender'),
		('D','undefined :)')
		)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	bio = models.CharField(max_length=400,null=True)
	gender = models.CharField(max_length=10,choices=gender_choice,default='D')
	age = models.IntegerField(default=1,validators=[MaxValueValidator(100),MinValueValidator(1)])


class PlayList(models.Model):
	name = models.CharField(max_length=160)
	picture = models.ImageField(upload_to='list_image',default='list_image/default.jpg')
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	music = models.ManyToManyField(Music)
	intro = models.CharField(max_length=300,null=True)
	date = models.DateTimeField(default=timezone.now)
	count = 0

	def __unicode__(self):
		return "Playlist: " + self.name + " Owner: " + self.user.username

	def update_count(self):
		count = self.music.count()


class Search(models.Model):
	search_user = models.CharField(max_length=400)
	search_song = models.CharField(max_length=400)

	def __unicode__(self):
		return "Search: " + self.keyword