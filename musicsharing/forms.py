from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput,TextInput, Textarea, FileInput
from django.contrib.auth.models import User
from musicsharing.models import *
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField,AutoCompleteField
from django.forms import extras
from django_countries.widgets import CountrySelectWidget
# class PostForm(forms.ModelForm):
# 	class Meta:
# 		model = Post
# 		fields = ['content']
# 		widgets = {'content': forms.Textarea(attrs={'placeholder':'New Post Here..','class':'new-post','cols':'100','rows':'3'})}

# 	def clean(self):
# 		cleaned_data = super(PostForm,self).clean()

# 		return cleaned_data

	
years = [x for x in range(1980,2017)]
class EditProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['age','gender','bio','date','country','nickname','picture']
		widgets = {'date':extras.SelectDateWidget(years=years, attrs={"class":"form-control"}),
		'country': CountrySelectWidget(attrs={"class":"form-control"}),
		'age': forms.TextInput(attrs={"class":"form-control"}),
		'bio': forms.TextInput(attrs={"class":"form-control"}),
		'nickname':forms.TextInput(attrs={"class":"form-control"}),
		'picture':forms.FileInput(attrs={'class':'custom-file-input file-input-wrapper btn btn-default btn-warning','id':"fileToUploadOne",'size':45})}
		# 'gender':forms.ChoiceField(attrs={"class":"form-control"})} #bug
	
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
		

	search_user = AutoCompleteField('search_user',required=False,help_text=None)


class SearchSongForm(forms.ModelForm):
	class Meta:
		model = Search
		fields = ['search_song']

	search_song = AutoCompleteField('search_song',required=False,help_text=None)


class AddSongForm(forms.ModelForm):
	class Meta:
		model = Search
		fields = ['add_song']

	add_song = AutoCompleteField('add_song',required=True,help_text=None)


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['content']

	music_name = forms.CharField(max_length=160)

	def clean(self):
		cleaned_data = super(PostForm,self).clean()

		return cleaned_data


# class CommentForm(forms.ModelForm):
# 	class Meta:
# 		model = Comment
# 		fields = ['content']

# 	def clean(self):
# 		cleaned_data = super(CommentForm,self).clean()

# 		return cleaned_data
		

	