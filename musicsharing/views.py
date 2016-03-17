from django.shortcuts import render, get_object_or_404, HttpResponse
from mimetypes import guess_type
from musicsharing.models import *

# Create your views here.

def default(request):
	return render(request,'home.html',{'music_name':'angshouxibeiwang'})

def get_audio(request,audio_name):
	music = get_object_or_404(Music,name=audio_name)

	content_type = guess_type(music.content.name)

	return HttpResponse(music.content,content_type=content_type)


def upload(request):
	new_music = Music(name=request.POST['name'],content=request.FILES['music'])

	new_music.save()

	return render(request,'home.html',{'music_name':request.POST['name']})