from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Music(models.Model):
	name = models.CharField(max_length=160)
	content = models.FileField(upload_to='music')

	def __unicode__(self):
		return self.name