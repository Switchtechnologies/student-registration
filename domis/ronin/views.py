from django.shortcuts import render
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.http import HttpResponse
from ronin.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
##Create your views here.
def index(request):
    return render(request, 'base.html')

def register(request):
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            registered = True
            
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()            
    return render(request, 'app_users/registeration.html',
                  {
                      'registered':registered,
                      'user_form':user_form,
                      'profile_form':profile_form
                  }
                  )
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('ACCOUNT IS DEACTIVATED')
        else:
            return HttpResponse('Please use correct id and password')
    return render(request, 'app_users/login.html')
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))            