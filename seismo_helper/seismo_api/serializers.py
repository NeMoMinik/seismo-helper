from rest_framework import serializers
from backend.models import Station, Location, Event, Trace, Corporation


class StationSerializer(serializers.ModelSerializer):
    traces = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Station
        fields = ('name', 'x', 'y', 'z', 'traces', 'location')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('name', 'corporation')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'x', 'y', 'z', 'start', 'end', 'magnitude')


class TraceSerializer(serializers.ModelSerializer):
    station = serializers.StringRelatedField(read_only=True)
    channels = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Trace
        fields = ('path', 'station', 'channels', 'event')


class CorporationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporation
        fields = ('name', )
