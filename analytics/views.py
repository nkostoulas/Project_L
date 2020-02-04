from django.shortcuts import render, redirect
from django.urls import reverse
from lists.models import UserTopList, UserProfile, Object, Category
from .forms import AnalyticsForm

# Create your views here.

def analytics_main(request):
    if request.method == 'POST':
        form = AnalyticsForm(request.POST)
        if form.is_valid():
            selected_object = form.cleaned_data['object']
            selected_attribute = form.cleaned_data['attribute']
            return redirect(reverse('analytics_selected', args=[Object.objects.get(name=selected_object).pk, selected_attribute]))
    else:
        form = AnalyticsForm()
    return render(request, 'analytics/analytics_main.html', {'current_nav': 'analytics', 'form': AnalyticsForm})

def analytics_selected(request,selected_object, selected_attribute):
    selected_object = Object.objects.get(pk=selected_object)
    form = AnalyticsForm(initial={'category':selected_object.category , 'object':selected_object, 'attribute':selected_attribute})
    attribute_array = get_data_array(selected_attribute, selected_object)

    return render(request, 'analytics/analytics_selected.html', {'current_nav': 'analytics', 'form': form, 'attribute_array': attribute_array, 'selected_category': selected_object.category, 'selected_object': selected_object, 'selected_attribute': selected_attribute})

def get_data_array(user_attribute, object):
    users_with_object_in_top = UserProfile.objects.filter(usertoplist__in = UserTopList.objects.filter(object=object))

    attribute_array = {}
    for user in users_with_object_in_top:
        attribute_value = get_attribute_value(user, user_attribute)
        if not attribute_array.get(attribute_value):
            attribute_array[attribute_value] = 1
        else:
            attribute_array[attribute_value] += 1

    return(attribute_array)

def get_attribute_value(user, user_attribute):
    return {
        'gender': user.gender,
        'locale': user.locale,
        'age_range': user.age_range,
    }[user_attribute]
