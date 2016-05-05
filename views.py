# -*- coding: utf-8 -*-"""

import json
from django.conf import settings
from django.http import HttpResponse
from conversejs.models import XMPPAccount
from conversejs.boshclient import BOSHClient
from utils import session_get_credentials, session_put_credentials


def bosh_prebind(request):
    print '--- bosh_prebind'
    jid, sid, rid = session_get_credentials(request)

    if jid and sid and rid:
        rid += 1
        request.session['rid'] = rid+1
        print 'existent credentials: ', jid, sid, rid
    else:
        xmpp_account = XMPPAccount.objects.get(user=request.user.pk)
        bosh = BOSHClient(xmpp_account.jid, xmpp_account.password,
                          settings.CONVERSEJS_BOSH_SERVICE_URL)
        jid, sid, rid = bosh.get_credentials()
        session_put_credentials(request, jid, sid, rid)
        print 'new credentials: ', jid, sid, rid
        
    return HttpResponse(json.dumps({'jid': jid, 'sid': sid, 'rid': rid}), content_type='application/json')
            