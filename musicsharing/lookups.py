from ajax_select import register, LookupChannel
from django.contrib.auth.models import User

@register('user')
class UserLookup(LookupChannel):

    model = User

    def get_query(self, q, request):
    	print q
        return self.model.objects.filter(username__icontains=q)

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.username