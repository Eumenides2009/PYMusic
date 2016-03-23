from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Music(models.Model):
	name = models.CharField(max_length=160,primary_key=True)
	content = models.FileField(upload_to='music')
	picture = models.ImageField(upload_to='music_image',default='music_image/default.jpg')
	user = models.ForeignKey(User,on_delete=models.CASCADE)

	def __unicode__(self):
		return "Music Name: " + self.name + "  Owner: " +self.user.username