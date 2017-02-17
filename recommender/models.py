from django.db import models
from lists.models import Object, UserProfile, Category

# Create your models here.
class RecommendationList(models.Model):
    object = models.ForeignKey(Object, on_delete = models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    @classmethod
    def create(cls, object, user, category):
        object = cls(object=object, user=user, category=category)
        return object

    def __str__(self):
        return "%s, %s, %s" % (self.user, self.object, self.category)

class UserLikeList(models.Model):
    object = models.ForeignKey(Object, on_delete = models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    @classmethod
    def create(cls, object, user, category):
        object = cls(object=object, user=user, category=category)
        return object

    def __str__(self):
        return "%s, %s, %s" % (self.user, self.object, self.category)

class UserDislikeList(models.Model):
    object = models.ForeignKey(Object, on_delete = models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    @classmethod
    def create(cls, object, user, category):
        object = cls(object=object, user=user, category=category)
        return object

    def __str__(self):
        return "%s, %s, %s" % (self.user, self.object, self.category)

class UserDiscardList(models.Model):
    object = models.ForeignKey(Object, on_delete = models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    @classmethod
    def create(cls, object, user, category):
        object = cls(object=object, user=user, category=category)
        return object

    def __str__(self):
        return "%s, %s, %s" % (self.user, self.object, self.category)
