
# import uuid

from django.conf import settings
import dmuc.conf
if settings.HAS_XMPP:
    from conversejs.models import XMPPAccount
    from conversejs.boshclient import BOSHClient
else:
    from .models import XMPPAccount
# from conversejs.xmpp import register_account

def session_get_credentials(request):
    session = request.session
    return session.get('jid', ''), session.get('sid', ''), session.get('rid', '')

def session_put_credentials(request, jid, sid, rid):
    request.session['jid'] = jid
    request.session['sid'] = sid
    request.session['rid'] = rid

def get_conversejs_context(context, xmpp_login=False):

    context['CONVERSEJS_ENABLED'] = conf.CONVERSEJS_ENABLED

    if not conf.CONVERSEJS_ENABLED:
        return context

    context.update(conf.get_conversejs_settings())

    request = context.get('request')
    if not xmpp_login or not request.user.is_active:
        return context

    request = context.get('request')
    xmpp_account = XMPPAccount.objects.get(user=request.user.pk)
    if settings.HAS_XMPP:
        bosh = BOSHClient(xmpp_account.jid, xmpp_account.password,
                          context['CONVERSEJS_BOSH_SERVICE_URL'])
        jid, sid, rid = bosh.get_credentials()
        bosh.close_connection()
        context.update({'jid': jid, 'sid': sid, 'rid': rid})
    return context
