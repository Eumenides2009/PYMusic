from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='modulus')
def modulus(value,args):
	value = int(value)
	mod,pos = args.split(",")
	mod = int(mod)
	pos = int(pos)


	if value % mod == 0 and pos == 0:
		return mark_safe('<div class="row">')
	elif value % mod == 2 and pos == 1:
		return mark_safe('</div>')
	else:
		return mark_safe('')
