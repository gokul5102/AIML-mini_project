# from django.db import models
# # Create your models here.
# class User(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     password1 = models.CharField(max_length=30)
#     password2 = models.CharField(max_length=30)

from django.db import models


class Query(models.Model):
    user = models.CharField(max_length=30)
    bat_team= models.CharField(max_length=30)
    bowl_team= models.CharField(max_length=30)
    overs = models.FloatField()
    runs = models.IntegerField()
    wickets = models.IntegerField()
    runs_in_prev_5 = models.IntegerField()
    wickets_in_prev_5 = models.IntegerField()
    logistic_result = models.IntegerField()
    random_forest_result = models.IntegerField()
    knn_result = models.IntegerField()
    def __str__(self):
        return self.user+" "+ self.bat_team +" "+ self.bowl_team

