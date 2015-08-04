# pylint: disable=W0613

from conversejs.models import XMPPAccount
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .core import create_room, delete_room, add_member, remove_member


class Room(models.Model):
    '''
    A MUC room. A corresponding room should exist on the XMPP server.
    '''


    name = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title


class RoomMember(models.Model):
    '''
    A room member association.
    '''


    xmpp_account = models.ForeignKey(XMPPAccount)
    room = models.ForeignKey(Room)

    def __unicode__(self):
        return "{} in {}".format(self.xmpp_account.jid, self.room.name)


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
