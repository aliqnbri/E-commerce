from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm ,RegisterForm  ,UserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


@login_required
def dashboard(request):
    return render (request, 'accounts/dashboard.html', {'section': 'dashboard'})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                email=cd['email'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Aurhenticate Successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            #Create New Cousom User but Avoid saving it 
            new_user = user_form.save(commit=False)
            # Set the Choosen Password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the Coustom Usert Object
            new_user.save()
            return render (request,'accounts/register_done.html',{'new_user': new_user})
    else:
        user_form = RegisterForm()
    return render(request,
                  'accounts/register.html',
                  {'user_form': user_form})        

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data = request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated '\
                                      'successfully')
        else:
            messages.error(request, 'Error updating your Account')    
    else:
        user_form = UserEditForm(instance=request.user)                    


    return render(request , 'accounts/edit.html',{'user_form':user_form})    