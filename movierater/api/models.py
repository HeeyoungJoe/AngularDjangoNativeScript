from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Movie(models.Model):
    #id를 까먹었다고 영상에 등장해서 임의로 넣은 줄
    id=models.PositiveIntegerField(primary_key=True)
    #viewset에서 rating을 확인하기 위해 내가 임의로 넣은 부분
    #Rating을 먼저 정의할 수 없어서 불가
    #stars=sum([star.stars for star in Rating.objects.filter(movie__id__contains=id)])

    #영상을 그대로 따라한 줄
    title=models.CharField(max_length=32)
    description=models.TextField(max_length=360)


    def no_of_rating(self):
        ratings=Rating.objects.filter(movie=self)

        return len(ratings)

    def avg_rating(self):
        sum=0
        ratings=Rating.objects.filter(movie=self)
        for rating in ratings:
            sum+=rating.stars

        if len(ratings)>0:
            return sum//len(ratings)
        else:
            return 0

class Rating(models.Model):
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    stars=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    class Meta:
        unique_together=(('user','movie'))
        index_together=(('user','movie'))