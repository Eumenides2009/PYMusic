from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
def validate_music_file(file):
	import os
	ext = os.path.splitext(file.name)[1]
	valid_extensions = ['.mp3','.flac']

	print ext

	if not ext in valid_extensions:
		raise ValidationError(u'Unsupported file extension.')

class Music(models.Model):
	name = models.CharField(max_length=160,primary_key=True)
	content = models.FileField(upload_to='music',validators=[validate_music_file])
	picture = models.ImageField(upload_to='music_image',default='music_image/default.jpg')
	user = models.ForeignKey(User,on_delete=models.CASCADE)


	def __unicode__(self):
		return "Music Name: " + self.name + "  Owner: " +self.user.username


class Profile(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	bio = models.CharField(max_length=400)
	