from django.shortcuts import render

from lists.models import UserTopList, UserProfile, Object, Category


# Create your views here.

def analytics_main(request):

    categories = Category.objects.filter(usertoplist__in = UserTopList.objects.all()).distinct()         # Categories with objects in top lists
    objects = Object.objects.filter(usertoplist__in = UserTopList.objects.all()).distinct()              # Objects in top lists

    return render(request, 'analytics/analytics_main.html', {'current_nav': 'analytics', 'categories': categories, 'objects': objects})


def analytics_selected(request,selected_object, selected_attribute):

    categories = Category.objects.filter(usertoplist__in = UserTopList.objects.all()).distinct()         # Categories with objects in top lists
    objects = Object.objects.filter(usertoplist__in = UserTopList.objects.all()).distinct()              # Objects in top lists

    selected_object = Object.objects.get(pk=selected_object)

    return render(request, 'analytics/analytics_selected.html', {'current_nav': 'analytics', 'selected_category': selected_object.category, 'selected_object': selected_object, 'selected_attribute': selected_attribute})

def get_data_array(user_attribute, object):
    print(user_attribute)
    users_with_object_in_top = UserProfile.objects.filter(usertoplist__in = UserTopList.objects.filter(object=object))

    attribute_array = {}
    for user in users_with_object_in_top:
        attribute_value = get_attribute_value(user, user_attribute)
        if not attribute_array.get(attribute_value):
            attribute_array[attribute_value] = 1
        else:
            attribute_array[attribute_value] += 1

    print(attribute_array)


def get_attribute_value(user, user_attribute):
    return {
        'gender': user.gender,
        'locale': user.locale,
        'age_range': user.age_range,
    }[user_attribute]
