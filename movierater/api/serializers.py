from rest_framework import serializers
from .models import Movie,Rating,User
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
#보안이 정말 허술함
#Post의 내용에 password가 고스란히 드러나있음
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','password')
        extra_kwards={'password':{'write_only':True,'required':True}}

    #존재하는 함수의 override에 해당함
    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        #새 user마다 새 token이 필요하므로 생성해준다.
        token=Token.objects.create(user=user)
        return user
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields=('id','title','description','no_of_rating','avg_rating')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rating
        fields=('id','stars','user','movie')

