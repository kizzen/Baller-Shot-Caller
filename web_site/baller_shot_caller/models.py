import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=25)
    join_date = models.DateTimeField()

    def did_user_recently_join(self):
        return self.join_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.name


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)