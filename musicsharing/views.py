import os
import logging
import httplib2

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from mimetypes import guess_type
from django.core import serializers
from musicsharing.models import *
import eyed3
import json

temp_upload_path = "/tmp/django_upload"
# Create your views here.

def get_music_metadata(file):
	with open(os.path.join(temp_upload_path,file.name),'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)

	meta = {}
	music = eyed3.load(os.path.join(temp_upload_path,file.name)) 

	meta['title'] = music.tag.title
	meta['author'] = music.tag.artist
	meta['album'] = music.tag.album

	print meta
	os.remove(os.path.join(temp_upload_path,file.name))

	return meta


@login_required
def home(request):
	return render(request,'home.html',{'music_name':'jianpoqinxin'})

@login_required
def get_audio(request,audio_name):
	music = get_object_or_404(Music,name=audio_name,user=request.user)

	content_type = guess_type(music.content.name)

	return HttpResponse(music.content,content_type=content_type)

@login_required
def get_picture(request,audio_name):
	music = get_object_or_404(Music,name=audio_name,user=request.user)

	content_type = guess_type(music.picture.name)

	return HttpResponse(music.picture,content_type=content_type)

@login_required
@transaction.atomic
def upload(request):
	
	if not request.FILES.get('music'):
		return render(request,'home.html',{})

	meta = get_music_metadata(request.FILES['music'])

	if not request.FILES.get('picture'):
		new_music = Music(name=meta['title'],artist=meta['author'],album=meta['album'],content=request.FILES['music'],user=request.user)
	else:
		new_music = Music(name=meta['title'],artist=meta['author'],album=meta['album'],content=request.FILES['music'],picture=request.FILES['picture'],user=request.user)
		
	new_music.save()	

	return render(request,'home.html',{})

@login_required
def get_audio_index(request):
	music_list = Music.objects.filter(user=request.user)
	name_list = []

	for music in music_list:
		new_meta = {}
		new_meta['title'] = music.name
		new_meta['author'] = music.artist
		new_meta['album'] = music.album

		name_list.append(new_meta)

	
	data = json.dumps({'name':name_list})

	return HttpResponse(data,content_type="application/json")


@login_required
def auth_return(request):
	pass

