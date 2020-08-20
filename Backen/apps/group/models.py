from django.db import models

class Group(models.Model):
    users = models.ManyToManyField()
class TeamPermission(models.Model):
    pass
class Team(models.Model):
    name = models.CharField()
    description = models.TextField()

# Create your models here.
