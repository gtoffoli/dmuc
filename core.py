import logging

from contextlib import contextmanager

from django.conf import settings

from sleekxmpp import ClientXMPP
from sleekxmpp.xmlstream import ET

SERVER = settings.XMPP_SERVER
ADMIN_USER = settings.XMPP_ADMIN_USER
ADMIN_PASS = settings.XMPP_ADMIN_PASSWORD
ADMIN_JID = '{}@{}'.format(ADMIN_USER, SERVER)
ROOM_DOMAIN = 'conference.' + SERVER

C = ClientXMPP(ADMIN_JID, ADMIN_PASS)
C.connected = False
C.register_plugin('xep_0133')
C.register_plugin('old_0004')
C.register_plugin('xep_0045')

DROP_CONNECTIONS = False

@contextmanager
def xmpp():
    try:
        if not C.connected or DROP_CONNECTIONS:
            C.connect()
            C.process()
            C.connected = True
        yield C
    finally:
        if DROP_CONNECTIONS:
            C.disconnect()
            C.connected = False

def create_user(username, password, name='', email=''):
    '''
    Connect to a server.
    '''

    with xmpp() as client:

        iq = client.makeIqSet(
            ET.Element('{http://jabber.org/protocol/commands}item', {
                'action': 'execute',
                'node': 'http://jabber.org/protocol/admin#add-user'
            })
        )
        iq['from'] = ADMIN_JID
        iq['to'] = SERVER
        iq['xml:lang'] = 'en'

        command = iq.send()['command']

        jid = '{}@{}'.format(username, SERVER)

        form = command['form']
        form.field['accountjid'].setValue(jid)
        form.field['password'].setValue(password)
        form.field['password-verify'].setValue(password)
        form.field['email'].setValue(email)
        form.field['given_name'].setValue(name)
        form.field['surname'].setValue('')

        del command['status']

        iq = client.makeIqSet(command)
        iq['from'] = ADMIN_JID
        iq['to'] = SERVER
        iq['xml:lang'] = 'en'
        result = iq.send()

        if 'Operation finished successfully' in str(result):
            return jid


def create_room(room, title):
    room = '{}@{}'.format(room, ROOM_DOMAIN)

    with xmpp() as client:
        muc = client.plugin['xep_0045']

        muc.joinMUC(room, ADMIN_USER, wait=True, pfrom=ADMIN_JID)
        form = muc.getRoomForm(room)

        if form:
            form.field['muc#roomconfig_roomname'].setValue(title)
            form.field['muc#roomconfig_roomdesc'].setValue(title)
            form.field['muc#roomconfig_persistentroom'].setValue('1')
            form.field['muc#roomconfig_membersonly'].setValue('1')
            form.field['muc#roomconfig_publicroom'].setValue('0')
            form.field['muc#roomconfig_maxusers'].setValue('0')
            muc.configureRoom(room, form=form, ifrom=ADMIN_USER)
            muc.leaveMUC(room, ADMIN_USER)
            return True

        muc.leaveMUC(room, ADMIN_USER)

def delete_room(room):
    room = '{}@{}'.format(room, ROOM_DOMAIN)

    with xmpp() as client:
        muc = client.plugin['xep_0045']
        muc.joinMUC(room, ADMIN_USER, wait=True, pfrom=ADMIN_JID)
        query = ET.Element('{http://jabber.org/protocol/muc#owner}query')
        item = ET.Element('{http://jabber.org/protocol/muc#owner}destroy')
        query.append(item)

        iq = client.makeIqSet(query)
        iq['to'] = room
        iq['from'] = client.boundjid

        iq.send()
        muc.leaveMUC(room, ADMIN_USER)

        return True


def set_affiliation(room, jid, affiliation):
    room = '{}@{}'.format(room, ROOM_DOMAIN)

    with xmpp() as client:
        muc = client.plugin['xep_0045']

        muc.joinMUC(room, ADMIN_USER, wait=True, pfrom=ADMIN_JID)
        query = ET.Element('{http://jabber.org/protocol/muc#admin}query')
        item = ET.Element('{http://jabber.org/protocol/muc#admin}item', {
            'affiliation': affiliation,
            'jid': jid,
            'nick': jid.split('@')[0]
        })
        query.append(item)

        iq = client.makeIqSet(query)
        iq['to'] = room
        iq['from'] = client.boundjid

        iq.send()
        muc.leaveMUC(room, ADMIN_USER)

        return True

def add_member(room, jid):
    return set_affiliation(room, jid, 'member')

def remove_member(room, jid):
    return set_affiliation(room, jid, 'none')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')
    assert create_room('test-room', 'Test')
    assert add_member('test-room', 'rohan@localhost')
    assert remove_member('test-room', 'rohan@localhost')
    assert delete_room('test-room')
