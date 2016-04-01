from ajax_select import register, LookupChannel
from django.contrib.auth.models import User
from musicsharing.models import *

@register('user')
class UserLookup(LookupChannel):

    model = User

    def get_query(self, q, request):
        return self.model.objects.filter(username__icontains=q)

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.username


@register('search_user')
class SearchUserLookup(LookupChannel):

	model = User

	def get_query(self, q, request):
		return self.model.objects.filter(username__icontains=q)

	def format_item_display(self,item):
		return u"<span class='tag'>%s</span>" % item.username


@register('search_song')
class SearchSongLookup(LookupChannel):

	model = Music

	def get_query(self,q,request):
		return self.model.objects.filter(name__icontains=q)

	def format_item_display(self,item):
		return u"<span class='tag'>%s</span>" % item.name