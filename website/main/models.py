from random import choices
from turtle import width
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    STATUS = (
        ('Losing Weight', 'Losing Weight'),
        ('Getting Stronger', 'Getting Stronger'),
    )

    userWithProfile = models.ForeignKey(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=100, default='')
    height = models.IntegerField()
    weight = models.IntegerField()
    goal = models.CharField(max_length=20, choices=STATUS, default='')

    def __str__(self):
        return self.fullName

class Workout(models.Model):
    nameWorkout = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        return str(self.id) + " " + self.nameWorkout
    