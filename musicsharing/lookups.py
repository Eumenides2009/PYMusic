from ajax_select import register, LookupChannel
from django.contrib.auth.models import User
from musicsharing.models import *
from django.db.models import Q

@register('user')
class UserLookup(LookupChannel):

    model = User

    def get_query(self, q, request):
        return self.model.objects.filter(username__icontains=q) 

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.username


@register('search_user')
class SearchUserLookup(LookupChannel):

	model = Profile

	def get_query(self, q, request):
		user = User.objects.filter(username__icontains=q)
		return self.model.objects.filter(Q(nickname__icontains=q)
										 | Q(user__in=user))


	def format_item_display(self,item): 
		return u"<span class='tag'>%s</span>" % (item.user.username)

	def format_match(self,item):
		return u"<span class='tag'>Nickname:%s   Username:%s</span>" % (item.nickname,item.user.username)


@register('search_song')
class SearchSongLookup(LookupChannel):

	model = Music

	def get_query(self,q,request):
		return self.model.objects.filter(name__icontains=q)

	def format_item_display(self,item):
		return u"<span class='tag'>%s</span>" % (item.name)

@register('add_song')
class AddSongLookup(LookupChannel):
	model = Music

	def get_query(self,q,request):
		return self.model.objects.filter(name__icontains=q, user=request.user)


	def format_item_display(self,item):
		return u"<span class='tag'>%s</span>" % (item.name)

@register('post_song')
class PostLookup(LookupChannel):
	model = Music

	def get_query(self,q,request):
		return self.model.objects.filter(name__icontains=q, user=request.user)

	def format_item_display(self,item):
		return u"<span class='tag'>%s</span>" % (item.name)