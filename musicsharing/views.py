import os
import logging
import httplib2

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, FileResponse
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from mimetypes import guess_type
from django.core import serializers
from musicsharing.models import *
from musicsharing.forms import *
import eyed3
import json
import chardet

temp_upload_path = "/tmp/django_upload"
# Create your views here.

def get_music_metadata(file):
	with open(os.path.join(temp_upload_path,file.name),'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)

	meta = {}
	music = eyed3.load(os.path.join(temp_upload_path,file.name))

	if music:
		meta['title'] = music.tag.title
		meta['author'] = music.tag.artist
		meta['album'] = music.tag.album

		if not meta['title']:
			meta['title'] = file.name

		print file.name

		os.remove(os.path.join(temp_upload_path,file.name))

	return meta


@login_required
def home(request):
	return render(request,'home.html',{})

# music section
@login_required
def get_audio(request,audio_name):
	music = get_object_or_404(Music,name=audio_name,user=request.user)

	start_pos = (int)(request.META['HTTP_RANGE'].split("=")[1].split("-")[0])

	music.content.seek(start_pos)

	response = FileResponse(music.content,status=206)
	response['Content-Length'] = music.content.size - start_pos
	response['Content-Type'] = 'audio/mpeg'
	response['Accept-Ranges'] = 'bytes'
	response['Content-Range'] = 'bytes %d-%d/%d' % (start_pos, music.content.size-1, music.content.size)
	response['Cache-Control'] = 'max-age:31556926'
 	response['Content-Disposition'] = 'attachment; filename=%s.mp3 ' % music.name.encode("utf8","ignore")
	
	return response

@login_required
def get_lyric(request,lyric_name):
	if request.method == 'POST':
		return HttpResponse(status=400)
	else:
		music = get_object_or_404(Music,name=lyric_name,user=request.user)

		if music.lyric:
			lyric = music.lyric.read()
			encoding = chardet.detect(lyric)
		else:
			return HttpResponse(status=404)

		return HttpResponse(json.dumps({'content':lyric},ensure_ascii=False),content_type='application/json;charset=' + encoding['encoding'])




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

	print meta

	if not meta:
		return render(request,'home.html',{})

	if not request.FILES.get('picture'):
		new_music = Music(name=meta['title'],artist=meta['author'],album=meta['album'],content=request.FILES['music'],user=request.user)
	else:
		new_music = Music(name=meta['title'],artist=meta['author'],album=meta['album'],content=request.FILES['music'],picture=request.FILES['picture'],user=request.user)
		
	if request.FILES.get('lyric'):
		new_music.lyric = request.FILES['lyric']

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

# profile section
@login_required
def profile(request,username):
	if request.method == 'POST':
		return reverse(views.home)
	else:
		try:
			user = User.objects.get(username=username)
			return render(request,'profile.html',{'user':user})
		except User.DoesNotExist:
			messages.info(request,'User ' + username + ' does not exists')
			return render(request,'home.html',{})


@login_required
def edit_profile(request):
	if request.method == 'GET':
		return reverse(views.profile,args=[request.user.username])
	else:
		try:
			profile = Profile.objects.get(user=request.user)		
		except Profile.DoesNotExist:
			profile = Profile()

		form = EditProfileForm(request.POST,instance=profile)

		if not form.is_valid():
			return render(request,'profile.html',{'form':form})
		
		form.save()

		return reverse(views.profile,args=[request.user.username])


# playlist section

@login_required
@transaction.atomic
def create_list(request):
	if request.method == 'GET':
		return render(request,"create_list.html",{})
	else:
		pass
	

@login_required
def get_list(request,list_name):
	pass

@login_required
@transaction.atomic
def delete_list(request,list_name):
	if request.method == 'POST':
		pass

@login_required
def auth_return(request):
	pass

