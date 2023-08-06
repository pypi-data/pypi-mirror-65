from django.conf.urls import url, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'polls', views.PollViewSet, basename='polls')
router.register(r'vote', views.VoteViewSet, basename='vote')

urlpatterns = [
    url(r'api/', include(router.urls)),
]
