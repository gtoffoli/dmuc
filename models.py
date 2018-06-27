# pylint: disable=W0613

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .core import create_room, delete_room, add_member, remove_member

from django.conf import settings
if settings.HAS_XMPP:
    from conversejs.models import XMPPAccount

class Room(models.Model):
    '''
    A MUC room. A corresponding room should exist on the XMPP server.
    '''


    name = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title
    def __str_(self):
        return self.__unicode__()

class RoomMember(models.Model):
    '''
    A room member association.
    '''


    if settings.HAS_XMPP:
        xmpp_account = models.ForeignKey(XMPPAccount, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __unicode__(self):
        return "{} in {}".format(self.xmpp_account.jid, self.room.name)
    def __str_(self):
        return self.__unicode__()

@receiver(post_save, sender=Room)
def after_room_create(instance, **kwargs):
    if kwargs.get('raw') or not kwargs.get('created'):
        return
    create_room(instance.name, instance.title)

@receiver(post_delete, sender=Room)
def after_room_delete(instance, **__):
    delete_room(instance.name)

@receiver(post_save, sender=RoomMember)
def after_room_member_create(instance, **kwargs):
    if kwargs.get('raw'):
        return
    add_member(instance.room.name, instance.xmpp_account.jid)

@receiver(post_delete, sender=RoomMember)
def after_room_member_delete(instance, **__):
    remove_member(instance.room.name, instance.xmpp_account.jid)
