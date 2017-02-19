from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to = 'category_backgrounds/')
    nav_url_slug = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Object(models.Model):

    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    url = models.URLField(max_length=200, blank=True)
    image = models.ImageField(upload_to='img/objectimages/' , blank=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):

    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name='profile')
    fbid = models.BigIntegerField(unique=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    locale = models.CharField(max_length=10, blank=True, null=True)
    age_range = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username

class UserTopList(models.Model):
    object = models.ForeignKey(Object, on_delete = models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    @classmethod
    def create(cls, object, user, category):
        object = cls(object=object, user=user, category=category)
        return object

    def __str__(self):
        return "%s, %s, %s" % (self.user, self.object, self.category)
