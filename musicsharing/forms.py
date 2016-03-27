from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput,TextInput, Textarea, FileInput
from django.contrib.auth.models import User
from musicsharing.models import *

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


# class CommentForm(forms.ModelForm):
# 	class Meta:
# 		model = Comment
# 		fields = ['content']

# 	def clean(self):
# 		cleaned_data = super(CommentForm,self).clean()

# 		return cleaned_data
		

	