from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'stations', views.GetStation, basename='stations')
router.register(r'locations', views.GetLocation, basename='locations')
router.register(r'events', views.GetEvent, basename='events')
router.register(r'traces', views.GetTrace, basename='traces')
router.register(r'corporation', views.GetCorporation, basename='corporations')

urlpatterns = [
    path('', include(router.urls)),
]
