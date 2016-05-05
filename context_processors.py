# from django.conf import settings
from conversejs.models import XMPPAccount
from models import RoomMember

def rooms(request):
    user = request.user
    rooms_count = 0
    if user.is_authenticated():
        try:
            xmpp_account = XMPPAccount.objects.get(user=user)
            rooms_count = RoomMember.objects.filter(xmpp_account=xmpp_account).count()
        except:
            pass
    return { 'rooms_count': rooms_count, }
