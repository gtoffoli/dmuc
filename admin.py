from django.contrib import admin
from .models import Room, RoomMember

class RoomMemberInline(admin.TabularInline):
    model = RoomMember

class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomMemberInline]

admin.site.register(Room, RoomAdmin)

class RoomMemberAdmin(admin.ModelAdmin):
    model = RoomMember

admin.site.register(RoomMember, RoomMemberAdmin)
