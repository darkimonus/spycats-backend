from django.urls import path, include
from rest_framework.routers import DefaultRouter
from missions.views import MissionViewSet, TargetViewSet

router = DefaultRouter()
router.register(r'missions', MissionViewSet, basename='mission')
router.register(r'targets', TargetViewSet, basename='target')

urlpatterns = [
    path('', include(router.urls)),
]
