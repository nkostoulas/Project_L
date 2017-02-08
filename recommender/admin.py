from django.contrib import admin
from .models import *

admin.site.register(RecommendationList)
admin.site.register(UserLikeList)
admin.site.register(UserDislikeList)
