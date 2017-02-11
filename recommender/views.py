from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from lists.models import UserTopList, UserProfile, Object, Category
from .models import RecommendationList, UserLikeList, UserDislikeList, UserDiscardList

@login_required
def remove_from_like(request, object):
	like = Object.objects.get(pk=object)
	like_object = UserLikeList.objects.get(object=like, user=request.user.profile).delete()
	recommender(request, like.category.pk)
	return redirect(reverse('user_list', args=[like.category.nav_url_slug]))

@login_required
def remove_from_dislike(request, object):
	dislike = Object.objects.get(pk=object)
	dislike_object = UserDislikeList.objects.get(object=dislike, user=request.user.profile).delete()
	recommender(request, dislike.category.pk)
	return redirect(reverse('user_list', args=[dislike.category.nav_url_slug]))

@login_required
def add_discard(request, object):
	user = request.user.profile
	discard = Object.objects.get(pk=object)

	discard_object = UserDiscardList.create(object=discard, user=user, category=discard.category)
	discard_object.save()

	like = UserLikeList.objects.filter(object=discard, user=user).delete()
	dislike = UserDislikeList.objects.filter(object=discard, user=user).delete()

	recommender(request, discard.category.pk)
	return redirect(reverse('user_list', args=[discard.category.nav_url_slug]))

@login_required
def add_like(request, object):

	user = request.user.profile
	like = Object.objects.get(pk=object)
	if UserLikeList.objects.filter(object=like, user=user).count() == 0:
		like_object = UserLikeList.create(object=like, user=user, category=like.category)
		like_object.save()

	dislike = UserDislikeList.objects.filter(object=like, user=user).delete()

	recommender(request, like.category.pk)
	return redirect(reverse('user_list', args=[like.category.nav_url_slug]))

@login_required
def add_dislike(request, object):

	user = request.user.profile
	dislike = Object.objects.get(pk=object)
	if UserDislikeList.objects.filter(object=dislike, user=user).count() == 0:
		dislike_object = UserDislikeList.create(object=dislike, user=user, category=dislike.category)
		dislike_object.save()

	like = UserLikeList.objects.filter(object=dislike, user=user).delete()

	recommender(request, dislike.category.pk)
	return redirect(reverse('user_list', args=[dislike.category.nav_url_slug]))

@login_required
def refresh_recommender(request, category):
	category = Category.objects.get(pk=category)
	discard_list = UserDiscardList.objects.filter(user=request.user.profile, category=category).delete()
	recommender(request, category.pk)
	return redirect(reverse('user_list', args=[category.nav_url_slug]))

@login_required
def recommender(request, category):

	user = request.user
	user_top_list = get_user_list(UserTopList.objects.filter(user=user.profile, category=category))
	user_like_list = get_user_list(UserLikeList.objects.filter(user=user.profile, category=category))
	user_dislike_list = get_user_list(UserDislikeList.objects.filter(user=user.profile, category=category))
	user_discard_list = get_user_list(UserDiscardList.objects.filter(user=user.profile, category=category))

	other_users = UserProfile.objects.exclude(user=user)
	other_user_choices = UserTopList.objects.filter(category=category).exclude(user = user.profile)
	other_top_list = get_other_user_list(other_users, other_user_choices)

	similarity_list = {}
	# Calculate similarity index with each other user
	for other_user, other_list in other_top_list.items():
		similarity_list[other_user] = calculate_similarity(user_top_list, other_list)

	# Sorted list of similarity scores
	similarity_list_sorted = sorted(similarity_list.items(), key=lambda x: x[1], reverse=True)

	# Recommendations based on similarity scores
	recommendations = choose_recommendations(user_top_list, user_like_list, user_dislike_list, user_discard_list, other_top_list, similarity_list_sorted)

	try:
		rec_1 = Object.objects.get(name=recommendations[0])
	except:
		rec_1 = None
	try:
		rec_2 = Object.objects.get(name=recommendations[1])
	except:
		rec_2 = None
	try:
		rec_3 = Object.objects.get(name=recommendations[2])
	except:
		rec_3 = None
	try:
		rec_4 = Object.objects.get(name=recommendations[3])
	except:
		rec_4 = None
	try:
		rec_5 = Object.objects.get(name=recommendations[4])
	except:
		rec_5 = None

	user_recommendations = RecommendationList.objects.filter(user=user.profile, category=category)
	category_object = Category.objects.get(pk=category)

	if user_recommendations.count() > 0:
		user_recommendations.update(recommendation_1=rec_1, recommendation_2=rec_2, recommendation_3=rec_3, recommendation_4=rec_4, recommendation_5=rec_5)
	else:
		recommendation_object = RecommendationList.create(recommendation_1=rec_1, recommendation_2=rec_2, recommendation_3=rec_3, recommendation_4=rec_4, recommendation_5=rec_5, user=user.profile, category=category_object)
		recommendation_object.save()

	return None

def calculate_similarity(user_list, other_list):
	similarity = 0

	for choice in other_list:
		if choice in user_list and choice != "":
			similarity += 1

	return similarity

def choose_recommendations(user_list, user_like_list, user_dislike_list, user_discard_list, other_user_lists, similarity_list):
	no_recommendations = 5
	recommendations = []

	for other_user, sim_score in similarity_list:
		if no_recommendations == 0:
			break

		if sim_score == 5:
			continue

		for choice in other_user_lists[other_user]:
			if choice not in user_list and \
			   choice not in user_like_list and \
			   choice not in recommendations and \
			   choice not in user_dislike_list and \
			   choice not in user_discard_list and \
			   choice != "":
				recommendations.append(choice)
				no_recommendations -= 1
			if no_recommendations == 0:
				break

	return recommendations

def get_user_list(user_objects):
	user_list = []
	for object in user_objects:
		user_list.append(object.object.name)
	return user_list

def get_other_user_list(users, user_objects):
	user_lists = {}
	for user in users:
		user_lists[user] = []

	for object in user_objects:
		user_lists[object.user].append(object)

	return user_lists
