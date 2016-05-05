
# import uuid

from django.conf import settings
import conf
from conversejs.models import XMPPAccount
from conversejs.boshclient import BOSHClient
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

    """
    try:
        xmpp_account = XMPPAccount.objects.get(user=request.user.pk)
    except XMPPAccount.DoesNotExist:
        jid_domain = conf.CONVERSEJS_AUTO_REGISTER
        if not jid_domain:
            return context

        xmpp_jid = request.user.username + u'@' + jid_domain
        xmpp_password = uuid.uuid4().hex # get a random uuid as password

        registered = register_account(xmpp_jid, xmpp_password,
                                      request.user.get_full_name(), request.user.email)

        if not registered:
            return context

        xmpp_account = XMPPAccount.objects.create(jid=xmpp_jid,
                                                  password=xmpp_password,
                                                  user=request.user)
        return context
    """
    print 'in conversejs_initialize'

    request = context.get('request')
    xmpp_account = XMPPAccount.objects.get(user=request.user.pk)
    """
    jid, sid, rid = session_get_credentials(request)
    if not context['CONVERSEJS_KEEPALIVE'] or not (jid and sid and rid):
    """
    if True:
        bosh = BOSHClient(xmpp_account.jid, xmpp_account.password,
                          context['CONVERSEJS_BOSH_SERVICE_URL'])
        jid, sid, rid = bosh.get_credentials()
        bosh.close_connection()
        """
        session_put_credentials(request, jid, sid, rid)
        """

    context.update({'jid': jid, 'sid': sid, 'rid': rid})
    return context
