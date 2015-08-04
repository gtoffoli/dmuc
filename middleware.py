import uuid
import logging

from conversejs.models import XMPPAccount
from django.contrib import messages

from .core import create_user

L = logging.getLogger(__name__)

def create_xmpp_account(request, user):
    '''
    Create a user's XMPP account if it doesn't already exist.
    '''
    if user.is_active and not user.xmpp.first():
        username = user.username
        password = str(uuid.uuid4())

        jid = create_user(username, password, user.get_full_name(),
                          user.email)
        if jid:
            xmpp_account = XMPPAccount.objects.create(user=user, jid=jid,
                                       password=password)
            messages.add_message(request, messages.SUCCESS,
                                 'Successfully created a XMPP account.')
        else:
            xmpp_account = None
            messages.add_message(request, messages.WARNING,
                                 'Failed to create a XMPP account.')

            L.error('Could not create a XMPP account for %s.', user)
        return xmpp_account

class UserXMPPMiddleware(object):

    def process_request(self, request):
        '''
        On each page request, create a user's XMPP account if it doesn't already exist.
        '''

        if request.path.startswith('/admin'):
            return

        user = request.user

        """
        if user.is_active and not user.xmpp.first():
            username = user.username
            password = str(uuid.uuid4())

            jid = create_user(username, password, user.get_full_name(),
                              user.email)
            if jid:
                XMPPAccount.objects.create(user=user, jid=jid,
                                           password=password)
                messages.add_message(request, messages.SUCCESS,
                                     'Successfully created a XMPP account.')
            else:
                messages.add_message(request, messages.WARNING,
                                     'Failed to create a XMPP account.')

                L.error('Could not create a XMPP account for %s.', user)
        """
        create_xmpp_account(request, user)
