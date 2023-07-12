from rest_framework import serializers
from backend.models import Station, Location, Event, Trace, Corporation, Channel


class StationSerializer(serializers.ModelSerializer):
    traces = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Station
        fields = ('name', 'x', 'y', 'z', 'traces', 'location', 'id')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('name', 'corporation', 'id')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'x', 'y', 'z', 'start', 'end', 'magnitude', 'location', 'id', 'traces')


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('path', )


class TraceSerializer(serializers.ModelSerializer):
    station = serializers.StringRelatedField(read_only=True)
    channels = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Trace
        fields = ('path', 'station', 'channels', 'event')


class PostTraceSerializer(serializers.ModelSerializer):
    channels = ChannelSerializer(many=True, )

    class Meta:
        model = Trace
        fields = ('path', 'station', 'channels', 'event', 'id')

    def create(self, validated_data):
        # print(validated_data)
        channels = validated_data.pop('channels')
        trace = Trace.objects.create(**validated_data)
        print(channels)
        for i in channels:
            c = Channel(path=i["path"], trace=trace)
            c.save()
        return trace


class CorporationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporation
        fields = ('name',)
