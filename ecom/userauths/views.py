from django.shortcuts import render, redirect
from userauths.forms import UserRegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User
# User = settings.AUTH_USER_MODEL
# Create your views here.

def register_view(request):
    if request.method == 'GET':
        form = UserRegistrationForm()
        return render(request, 'userauths/sign-up.html', {'form': form})
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, Account created successfully")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
                                    )
            login(request, new_user)
            print(new_user)
            return redirect('core:index')
    else:
        messages.error(request, f" somthing went wrong")
        
        print("something went wrong")
        return render(request, "userauths/sign-up.html",context)

    context = {
        'form':form,
    }
    return render(request, "userauths/sign-up.html",context)


def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, f"Hey You are already Logged In")
        
        return redirect("core:index")
    
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email) 
            user = authenticate(request,email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request,f"You are logged in")
                return redirect("core:index")
            else:
                messages.warning(request, "User doesn't exist, create an account")
        except:
            messages.warning(request, f"User with {email} doesn't exist")
        
        
    
    return render(request, "userauths/sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request, f"You Have Logged Out")
    
    return redirect( "userauths:sign-in")