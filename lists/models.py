from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Object(models.Model):

    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):

    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=20, blank=True, null=True)
    locale = models.CharField(max_length=10, blank=True, null=True)
    age_range = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Choice(models.Model):

    name = models.ForeignKey(Object, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #category = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    @classmethod
    def create(cls, name, user):
        choice = cls(name=name, user=user, category=name.category)
        return choice

    def __str__(self):
        return "%s, %s, %s" % (self.user, self.name, self.name.category)
