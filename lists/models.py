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

    choice_1 = models.ForeignKey(Object, on_delete = models.CASCADE, related_name='choice_1')
    choice_2 = models.ForeignKey(Object, on_delete = models.CASCADE, related_name='choice_2')
    choice_3 = models.ForeignKey(Object, on_delete = models.CASCADE, related_name='choice_3')
    choice_4 = models.ForeignKey(Object, on_delete = models.CASCADE, related_name='choice_4')
    choice_5 = models.ForeignKey(Object, on_delete = models.CASCADE, related_name='choice_5')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    @classmethod
    def create(cls, choice_1, choice_2, choice_3, choice_4, choice_5, user):
        choice = cls(choice_1=choice_1, choice_2=choice_2, choice_3=choice_3, choice_4=choice_4, choice_5=choice_5,
                     user=user, category=choice_1.category)
        return choice

    def __str__(self):
        return "%s, %s, %s, %s" % (self.user, self.choice_1.category)
