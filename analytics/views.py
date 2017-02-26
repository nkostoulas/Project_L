from django.shortcuts import render

from lists.models import UserTopList, UserProfile, Object, Category


# Create your views here.

def get_data_array(request,user_attribute, object):
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

    return render(request, 'projectl/home.html')


def get_attribute_value(user, user_attribute):
    return {
        'gender': user.gender,
        'locale': user.locale,
        'age_range': user.age_range,
    }[user_attribute]
