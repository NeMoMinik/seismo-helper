from django.contrib import admin
from .models import Corporation, Location, Event, Station, Trace, Channel


@admin.register(Corporation)
class CorporationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Event)
class CorporationAdmin(admin.ModelAdmin):
    list_display = ('id', 'x', 'y', 'z', 'magnitude', 'time')


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'x', 'y', 'z')


@admin.register(Trace)
class TraceAdmin(admin.ModelAdmin):
    list_display = ('id', 'path', 'start', 'end')


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'path')
