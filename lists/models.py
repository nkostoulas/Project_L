from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Object(models.Model):

    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Category)
    description = models.TextField()
    url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Choice(models.Model):
    
    choice = models.ForeignKey(Object, null=True)
    user = models.ForeignKey('auth.User')

    def __str__(self):
        return "%s, %s, %s" % (self.user, self.choice, self.choice.category)

