from django.db import models
from lists.models import Object, UserProfile, Category

# Create your models here.
class RecommendationList(models.Model):

    recommendation_1 = models.ForeignKey(Object, on_delete = models.CASCADE, related_name='recommendation_1', null=True)
    recommendation_2 = models.ForeignKey(Object, on_delete = models.CASCADE, related_name='recommendation_2', null=True)
    recommendation_3 = models.ForeignKey(Object, on_delete = models.CASCADE, related_name='recommendation_3', null=True)
    recommendation_4 = models.ForeignKey(Object, on_delete = models.CASCADE, related_name='recommendation_4', null=True)
    recommendation_5 = models.ForeignKey(Object, on_delete = models.CASCADE, related_name='recommendation_5', null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    @classmethod
    def create(cls, recommendation_1, recommendation_2, recommendation_3, recommendation_4, recommendation_5, user, category):
        recommendations = cls(recommendation_1=recommendation_1, recommendation_2=recommendation_2, recommendation_3=recommendation_3,
        			recommendation_4=recommendation_4, recommendation_5=recommendation_5, user=user, category=category)
        return recommendations

    def __str__(self):
        return "%s, %s" % (self.user, self.category)

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
