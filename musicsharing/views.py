import os
import logging
import httplib2

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404
from mimetypes import guess_type
from musicsharing.models import *

from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_orm import Storage

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secrets.json')

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/plus.me',
    redirect_uri='http://localhost:8000/oauth2callback')

# Create your views here.

def home(request):
	return render(request,'home.html',{'music_name':'jianpoqinxin'})

def get_audio(request,audio_name):
	music = get_object_or_404(Music,name=audio_name)

	content_type = guess_type(music.content.name)

	return HttpResponse(music.content,content_type=content_type)


def upload(request):
	new_music = Music(name=request.POST['name'],content=request.FILES['music'])

	new_music.save()

	return render(request,'home.html',{'music_name':request.POST['name']})


def auth_return(request):
	pass
