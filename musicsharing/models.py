from __future__ import unicode_literals
import os
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django_countries.fields import CountryField
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
		('T','Transgender'),
		('D','undefined :)')
		)
	user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='profile')
	bio = models.CharField(max_length=400,null=True,blank=True)
	gender = models.CharField(max_length=10,choices=gender_choice,default='D',blank=True)
	date = models.DateField(null=True,blank=True)
	age = models.IntegerField(default=1,validators=[MaxValueValidator(100),MinValueValidator(1)],blank=True,null=True)
	country = CountryField(blank_label='(select country)',null=True,blank=True)
	picture = models.ImageField(upload_to='profile_image',blank=True,default="profile_image/default.jpg")
	nickname = models.CharField(max_length=30,null=True,blank=True)
	friends = models.ManyToManyField(User,related_name='friends')

class Post(models.Model):
	content = models.CharField(max_length=140)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	music = models.ForeignKey(Music,on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now=True)

class Comment(models.Model):
	content = models.CharField(max_length=140)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	post = models.ForeignKey(Post,on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now=True)

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
		self.count = self.music.count()


class Search(models.Model):
	search_user = models.CharField(max_length=100)
	search_song = models.CharField(max_length=100)
	add_song = models.CharField(max_length=100)
	post_song = models.CharField(max_length=100)

	def __unicode__(self):
		return "Search: " + self.keyword 


# signal functions that delete files when associated model instance is deleted
@receiver(models.signals.post_delete, sender=Music)
@receiver(models.signals.post_delete, sender=Profile)
@receiver(models.signals.post_delete, sender=PlayList)
def auto_delete_file_on_delete(sender, instance, **kwargs):
	if sender.__name__ == 'Music':
		if instance.content:
			if os.path.isfile(instance.content.path):
				os.remove(instance.content.path)

		if instance.lyric:
			if os.path.isfile(instance.lyric.path):
				os.remove(instance.lyric.path)


	if instance.picture and instance.picture.name != 'list_image/default.jpg' and instance.picture.name != 'profile_image/default.jpg':
		if os.path.isfile(instance.picture.path):
			os.remove(instance.picture.path)

	

