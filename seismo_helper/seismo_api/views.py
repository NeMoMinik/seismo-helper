from backend.models import Station, Location, Event, Trace, Corporation
from .serializers import StationSerializer, LocationSerializer, EventSerializer, TraceSerializer, CorporationSerializer, PostTraceSerializer
from rest_framework import viewsets


class GetStation(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class GetLocation(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class GetEvent(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class GetTrace(viewsets.ModelViewSet):
    queryset = Trace.objects.all()
    # serializer_class = TraceSerializer

    def get_serializer_class(self):
        print(self.request.POST)
        if self.request.method == "GET":
            return TraceSerializer
        else:
            return PostTraceSerializer


class GetCorporation(viewsets.ModelViewSet):
    queryset = Corporation.objects.all()
    serializer_class = CorporationSerializer
