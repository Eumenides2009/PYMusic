from django import template


register = template.Library()

@register.filter(name='modulus')
def modulus(value,mod):
	return value % mod
