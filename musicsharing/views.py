import os
import logging
import httplib2

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, FileResponse
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.contrib import messages
from mimetypes import guess_type
from django.core import serializers
from allauth.account.signals import user_signed_up,user_logged_in
from musicsharing.models import *
from musicsharing.forms import *
import eyed3
import json
import chardet

temp_upload_path = "/tmp/django_upload"

def add_profile(**kwargs):
	try:
		profile = Profile.objects.get(user=kwargs['request'].user)
	except Profile.DoesNotExist:
		profile = Profile(user=kwargs['request'].user)
		profile.save()
		print 'add new profile'
	

user_signed_up.connect(add_profile)
user_logged_in.connect(add_profile)

# Create your views here.

def get_music_metadata(file):
	with open(os.path.join(temp_upload_path,file.name),'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)

	meta = {}
	music = eyed3.load(os.path.join(temp_upload_path,file.name))

	if music:
		if music.tag:
			meta['title'] = music.tag.title
			meta['author'] = music.tag.artist
			meta['album'] = music.tag.album

			if not meta['title']:
				meta['title'] = file.name.split('.')[0]

		else:
			meta['title'] = file.name.split('.')[0]
			meta['author'] = None
			meta['album'] = None

		print file.name

		os.remove(os.path.join(temp_upload_path,file.name))

	return meta


@login_required
def home(request):
	list_id = 0
	if request.method == 'GET' and request.GET.get('id',''):
		list_id = request.GET.get('id')
	
	print list_id
	return TemplateResponse(request,'home.html',{'list_id':list_id})

@login_required
def friend_stream(request):
	return TemplateResponse(request,'friend_stream.html',{})

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
		return TemplateResponse(request,'home.html',{'list_id':0})

	meta = get_music_metadata(request.FILES['music'])

	if not meta:
		return TemplateResponse(request,'home.html',{'list_id':request.POST['list_id']})

	if not request.FILES.get('picture'):
		new_music = Music(name=meta['title'],artist=meta['author'],album=meta['album'],content=request.FILES['music'],user=request.user)
	else:
		new_music = Music(name=meta['title'],artist=meta['author'],album=meta['album'],content=request.FILES['music'],picture=request.FILES['picture'],user=request.user)
		
	if request.FILES.get('lyric'):
		new_music.lyric = request.FILES['lyric']

	new_music.save()	

	if request.POST.get('playlist'):
		try:
			playlist = PlayList.objects.get(name=request.POST['playlist'])
			playlist.music.add(new_music)
			playlist.update_count()
			playlist.save()
		except PlayList.DoesNotExist:
			pass

	return TemplateResponse(request,'home.html',{'list_id':request.POST['list_id']})

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
		profile = Profile.objects.get(user=request.user)
		return TemplateResponse(request,'profile.html',{'profile':profile})
	else:
		try:
			profile = Profile.objects.get(user__username=username)
			return TemplateResponse(request,'profile.html',{'profile':profile})
		except Profile.DoesNotExist:
			if username != "":
				messages.info(request,'User ' + username + ' does not exists')
			profile = Profile.objects.get(user=request.user)
			return TemplateResponse(request,'profile.html',{'profile':profile})


@login_required
def edit_profile(request):
	if request.method == 'GET':
		e_profile = Profile.objects.get(user=request.user)
		form = EditProfileForm(instance=e_profile)
		return TemplateResponse(request,'edit_profile.html',{'form':form})
	else:
		try:
			e_profile = Profile.objects.get(user=request.user)		
		except Profile.DoesNotExist:
			e_profile = Profile()

		form = EditProfileForm(request.POST,request.FILES,instance=e_profile)

		if not form.is_valid():
			return TemplateResponse(request,'edit_profile.html',{})
		
		form.save()

		return redirect('profile',username='')

@login_required
def get_profile_picture(request,profile_id):
	if request.method == 'POST':
		return HttpResponse(status=400)
	else:
		profile = get_object_or_404(Profile,id=profile_id)

		if not profile.picture:
			return HttpResponse(status=404)

		return HttpResponse(profile.picture,content_type=guess_type(profile.picture.name))

# song section

@login_required
def manage_songs(request):
	song_list = Music.objects.filter(user=request.user)
	return TemplateResponse(request,'manage_songs.html',{'song_list':song_list})

@login_required
@transaction.atomic
def remove_song_repo(request):
	if request.method == 'GET':
		return redirect('manage_songs')
	else:
		if request.POST.get('song_name'):
			try:
				music = Music.objects.get(name=request.POST['song_name'],user=request.user)
				music.delete()
				return redirect('manage_songs')
			except Music.DoesNotExist:
				return redirect('manage_songs')
		else:
			return redirect('manage_songs')

def edit_song(request):
	if request.method == 'GET' or not request.POST.get('origin_name'):
		return HttpResponse(status=400)
	else:
		try:
			music = Music.objects.get(name=request.POST['origin_name'],user=request.user)

			if request.POST.get('title'):
				music.title = request.POST['title']

			if request.POST.get('author'):
				music.artist = request.POST['author']

			if request.POST.get('album'):
				music.alum = request.POST['album']
		except Music.DoesNotExist:
			return HttpResponse(status=404)

# playlist section


@login_required
def playlist(request):
	playlist_collection = PlayList.objects.filter(user=request.user)
	for i in playlist_collection:
		i.update_count()
	return TemplateResponse(request,'playlist.html',{'playlist':playlist_collection})



@login_required
@transaction.atomic
def edit_playlist(request):
	if request.method == 'GET':
		return redirect('playlist')
	else:
		if not request.POST.get('list_id'):
			return redirect('playlist')
		else:
			try:
				m_playlist = PlayList.objects.get(id=request.POST['list_id'],user=request.user)

				if request.POST.get('list_name'):
					m_playlist.name = request.POST['list_name']

				if request.POST.get('list_intro'):
					m_playlist.intro = request.POST['list_intro']

				m_playlist.save()

				return redirect('playlist')

			except PlayList.DoesNotExist:
				return redirect('playlist')

	

@login_required
@transaction.atomic
def create_list(request):
	if request.method == 'GET':
		return redirect('playlist')
	else:
		new_list = PlayList(user=request.user)
		form = AddPlayListForm(request.POST,request.FILES,instance=new_list)

		if not form.is_valid():
			print form.errors
			return redirect('playlist')

		form.save()

		playlist_collection = PlayList.objects.filter(user=request.user)
		return redirect('playlist')
	

@login_required
def get_list(request,list_id):
	if request.method == 'POST':
		return HttpResponse(status=400)
	else:
		if list_id == '0':
			return get_audio_index(request)
		else:
			try:
				playlist = PlayList.objects.get(id=list_id,user=request.user)
				name_list = []

				for music in playlist.music.all():
					new_meta = {}
					new_meta['title'] = music.name
					new_meta['author'] = music.artist
					new_meta['album'] = music.album

					name_list.append(new_meta)
		
				data = json.dumps({'name':name_list})
				return HttpResponse(data,content_type='application/json')

			except PlayList.DoesNotExist:
				return HttpResponse(status=404)

@login_required
def get_list_name(request):
	playlist = PlayList.objects.filter(user=request.user)
	name_list = []

	for  i in playlist:
		name_list.append(i.name)

	return HttpResponse(json.dumps({'name':name_list}),content_type='application/json')

@login_required
def get_list_picture(request,list_id):
	if request.method == 'POST':
		return HttpResponse(status=400)
	else:
		try:
			playlist = PlayList.objects.get(id=list_id,user=request.user)
			return HttpResponse(playlist.picture,content_type=guess_type(playlist.picture.name))

		except PlayList.DoesNotExist:
			return HttpResponse(status=404)

@login_required
@transaction.atomic
def delete_list(request):
	if request.method == 'GET':
		return redirect('playlist')
	else:
		if request.POST.get('list_id'):
			try:
				todelete = PlayList.objects.get(id=request.POST['list_id'],user=request.user)
				todelete.delete()
				return redirect('playlist')
			except PlayList.DoesNotExist:
				return redirect('playlist')
		else:
			return redirect('playlist')


# song in list
@login_required
@transaction.atomic
def delete_song(request):
	if request.method == 'GET':
		return HttpResponse(status=400)
	else:
		if not request.POST.get('list_id') or not request.POST.get('song_name'):
			return HttpResponse(status=400)
		else:
			try:
				playlist = PlayList.objects.get(id=request.POST['list_id'],user=request.user)
				try:
					music_to_delete = playlist.music.get(name=request.POST['song_name'])
					playlist.music.remove(music_to_delete)
					playlist.save()
					return HttpResponse(status=200)
				except Music.DoesNotExist:					
					return HttpResponse(status=404)
			except PlayList.DoesNotExist:
				return HttpResponse(status=404)

@login_required
@transaction.atomic
def add_song(request):
	if request.method == 'GET':
		return HttpResponse(status=400)
	else:
		if not request.POST.get('list_id') or not request.POST.get('song_name'):
			return HttpResponse(status=400)
		else:
			try:
				playlist = PlayList.objects.get(id=request.POST['list_id'],user=request.user)
				try:
					music = Music.objects.get(name=request.POST['song_name'],user=request.user)
					playlist.music.add(music)
					playlist.save()
					return HttpResponse(status=200)
				except Music.DoesNotExist:
					return HttpResponse(status=404) 
			except PlayList.DoesNotExist:
				return HttpResponse(status=404)

# search section
@login_required
def search(request):
	if request.method == 'POST':
		return redirect('home')
	else:
		if request.GET['selecter_basic'] == '1':
			return redirect('profile',username=request.GET['search_user'])
		else:			
			return redirect('home')

# friend section
@login_required
@transaction.atomic
def follow(request,username):
	if request.method == 'GET':
		return redirect('profile',username="")
	else:
		try:
			user = User.objects.get(username=username)
			profile = Profile.objects.get(user=request.user)
			profile.friends.add(user)
			profile.save()
			return redirect('profile',username="")
		except User.DoesNotExist:
			return redirect('profile',username="")


@login_required
@transaction.atomic
def unfollow(request,username):
	if request.method == 'GET':
		return redirect('profile',username="")
	else:
		try:
			user = User.objects.get(username=username)
			profile = Profile.objects.get(user=request.user)
			profile.friends.remove(user)
			profile.save()
			return redirect('profile',username="")
		except User.DoesNotExist:
			return redirect('profile',username="")





@login_required
def auth_return(request):
	pass

