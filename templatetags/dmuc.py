
from django import template
from ..utils import get_conversejs_context

register = template.Library()
TEMPLATE_PATH = 'dmuc/includes/'

@register.inclusion_tag(TEMPLATE_PATH + 'initialize.html', takes_context=True)
def dmuc_conversejs_initialize(context):
    return get_conversejs_context(context, xmpp_login=True)
