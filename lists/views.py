from django.shortcuts import render

# Create your views here.

def user_list(request):

    return render(request, 'lists/user_list.html')