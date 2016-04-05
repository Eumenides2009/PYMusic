from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput,TextInput, Textarea, FileInput
from django.contrib.auth.models import User
from musicsharing.models import *
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField,AutoCompleteField

# class PostForm(forms.ModelForm):
# 	class Meta:
# 		model = Post
# 		fields = ['content']
# 		widgets = {'content': forms.Textarea(attrs={'placeholder':'New Post Here..','class':'new-post','cols':'100','rows':'3'})}

# 	def clean(self):
# 		cleaned_data = super(PostForm,self).clean()

# 		return cleaned_data

	

class EditProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['age','gender','bio']
	
	def clean(self):
		cleaned_data = super(EditProfileForm,self).clean()

		return cleaned_data

class AddPlayListForm(forms.ModelForm):
	class Meta:
		model = PlayList
		fields = ['name','intro','picture']

	def clean(self):
		cleaned_data = super(AddPlayListForm,self).clean()

		return cleaned_data


class SearchUserForm(forms.ModelForm):
	class Meta:
		model = Search
		fields = ['search_user']
		widgets = {'search_user': TextInput(attrs={'class':'form-control search-query'})}

	search_user = AutoCompleteField('search_user',required=False,help_text=None)


class SearchSongForm(forms.ModelForm):
	class Meta:
		model = Search
		fields = ['search_song']
		widgets = {'search_song': TextInput(attrs={'class':'form-control search-query'})}

	search_song = AutoCompleteField('search_song',required=False,help_text=None)



# class CommentForm(forms.ModelForm):
# 	class Meta:
# 		model = Comment
# 		fields = ['content']

# 	def clean(self):
# 		cleaned_data = super(CommentForm,self).clean()

# 		return cleaned_data
		

	