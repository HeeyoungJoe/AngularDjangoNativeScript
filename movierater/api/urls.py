from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import MovieViewSet,RatingViewSet,UserViewSet

'''
rest_framework 

router를 통해 url을 유동적으로 관리할 수 있다. 
'''
router = routers.DefaultRouter()
router.register('user',UserViewSet)
router.register('movies',MovieViewSet)
router.register('ratings',RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
