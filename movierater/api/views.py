from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.decorators import action
from .models import Movie,Rating
from .serializers import MovieSerializer,RatingSerializer,UserSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
#view per serializer

class UserViewSet(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class=UserSerializer #하나만 가능


class MovieViewSet(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer #하나만 가능
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,)

    '''
    POST를 할 때 주고받는 정보를 정의한다.
    Serializer 레이어를 거친 것을 받으므로 그쪽에서 정의한 것만 가지고 변형할 수 있다.
    '''
    @action(detail=True,methods=['POST']) #accept POST only, and show details as default
    def rate_movie(self,request,pk=None):
        if 'stars' in request.data: #Movie에 대한 post는 stars를 가지지 않아 아직 드러나지 않는다.

            movie=Movie.objects.get(id=pk)
            stars=request.data['stars']
            user=request.user #택 1 중 1
            #user=User.objects.get(id=1) #택 1 중 2
            print('user',user)

            try:
                rating=Rating.objects.get(user=user,movie=movie.id)
                rating.stars=stars
                rating.save()
                serializer=RatingSerializer(rating,many-False)
                response={'message':'Rating updated','result':serializer.data}
                return Response(response,status=status.HTTP_200_OK)
            except:
                rating=Rating.objects.create(user=user, movie=movie.id,stars=stars)
                serializer = RatingSerializer(rating, many - False)
                response = {'message': 'Rating updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)


        else:
            response={'message':'You need to provide stars'}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
    def update(self,request,*args,**kwargs):
        response={'message':'You can\'t update rating like that'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets.ModelViewSet):
    queryset=Rating.objects.all()
    serializer_class=RatingSerializer #하나만 가능

    #disable을 위한 overriding
    def update(self,request,*args,**kwargs):
        response={'message':'You can\'t update rating like that'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)

    def create(self,request,*args,**kwargs):
        response={'message':'You can\'t create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
