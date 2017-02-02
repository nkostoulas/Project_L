from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from lists.models import UserChoiceList, UserProfile, Object
from .models import RecommendationList

@login_required
def recommender(request, category):

	user = request.user
	user_list = get_user_list(UserChoiceList.objects.get(user = user.profile, category=category))
	other_user_lists = UserChoiceList.objects.filter(category=category).exclude(user = user.profile)
	similarity_list = {}

	# Calculate similarity index with each other user
	for other in other_user_lists:
		other_list = get_user_list(other)
		other_name = other.user.user.username
		similarity_list[other_name] = calculate_similarity(user_list, other_list)

	# Sorted list of similarity scores
	similarity_list_sorted = sorted(similarity_list.items(), key=lambda x: x[1], reverse=True)
	
	# Recommendations based on similarity scores	
	recommendations = choose_recommendations(user_list, other_user_lists, similarity_list_sorted)

	rec_1 = Object.objects.get(name=recommendations[0])
	rec_2 = Object.objects.get(name=recommendations[1])
	rec_3 = Object.objects.get(name=recommendations[2])
	rec_4 = Object.objects.get(name=recommendations[3])
	rec_5 = Object.objects.get(name=recommendations[4])
	
	user_recommendations = RecommendationList.objects.filter(user=user.profile, category=category)

	if user_recommendations.count() > 0:
		user_recommendations.update(recommendation_1=rec_1, recommendation_2=rec_2, recommendation_3=rec_3, recommendation_4=rec_4, recommendation_5=rec_5)
	else:
		recommendation_object = RecommendationList.create(recommendation_1=rec_1, recommendation_2=rec_2, recommendation_3=rec_3, recommendation_4=rec_4, recommendation_5=rec_5, user=user.profile)
		recommendation_object.save()

	return None
	#return render(request, 'recommender/recommender.html', {'similarity_list': similarity_list_sorted, 'recommendations': recommendations})

def calculate_similarity(user_list, other_list):
	similarity = 0

	for choice in other_list:
		if choice in user_list and choice != "":
			similarity += 1

	return similarity

def choose_recommendations(user_list, other_user_lists, similarity_list):
	no_recommendations = 5
	recommendations = []

	for similarity in similarity_list:
		other_user = similarity[0]
		sim_score = similarity[1]

		if no_recommendations == 0:
			break

		if sim_score == 5:
			continue

		other_list = get_user_list(other_user_lists.get(user=UserProfile.objects.get(user=User.objects.get(username=other_user))))
		
		for choice in other_list: 
			print(choice)
			if choice not in user_list and choice != "" and choice not in recommendations :
				recommendations.append(choice)
				no_recommendations -= 1
			if no_recommendations == 0:
				break

	return recommendations

def get_user_list(user_list):

	if user_list.choice_1 == None:
		choice_1 = ""
	else:
		choice_1 = user_list.choice_1.name

	if user_list.choice_2 == None:
		choice_2 = ""
	else:
		choice_2 = user_list.choice_2.name

	if user_list.choice_3 == None:
		choice_3= ""
	else:
		choice_3 = user_list.choice_3.name

	if user_list.choice_4 == None:
		choice_4 = ""
	else:
		choice_4 = user_list.choice_4.name

	if user_list.choice_5 == None:
		choice_5 = ""
	else:
		choice_5 = user_list.choice_5.name

	return [choice_1, choice_2, choice_3, choice_4, choice_5]

