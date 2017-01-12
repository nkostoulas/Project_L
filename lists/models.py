from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class Object(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category)

    def _str_(self):
        return self.name
