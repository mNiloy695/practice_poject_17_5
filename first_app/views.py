from django.shortcuts import render,redirect
from .forms import UserForm,ChangeForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash


# Create your views here.
def signup(request):
   if not request.user.is_authenticated:
        if request.method=='POST':
           user_form=UserForm(request.POST)
           if user_form.is_valid():
            user_form.save()
            messages.success(request,"Your account successfully created")
            print(user_form.cleaned_data)
            return redirect('add_user')
        else:
           user_form=UserForm()
        return render(request,'signup.html',{'form':user_form})
   else:
       return redirect('profile')
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            user_form=AuthenticationForm(request=request,data=request.POST)
            if user_form.is_valid():
                 name=user_form.cleaned_data['username']
                 user_pass=user_form.cleaned_data['password']
                 user=authenticate(username=name , password=user_pass)
                 if user is not None:
                     login(request,user)
                     return redirect('profile')
        else:
          user_form=AuthenticationForm()
        return render(request,'login.html',{'form':user_form})
    else:
        return redirect('profile')
    

def profile(request):
    if request.user.is_authenticated:
        if request.method=='POST':
           user_form=ChangeForm(request.POST,instance=request.user)
           if user_form.is_valid():
            user_form.save()
            messages.success(request,"You successfully Updated your profile")
            return redirect('profile')
        else:
           user_form=ChangeForm(instance=request.user)
        return render(request,'profile.html',{'form':user_form})
    else:
        return redirect('login')
def user_logout(request):
    logout(request)
    return redirect('login')
def change_password(request):
    if request.method=='POST':
         form=PasswordChangeForm(user=request.user,data=request.POST)
         if form.is_valid():
             form.save()
             update_session_auth_hash(request,form.user)
             return redirect('profile')
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,'change_pass.html',{'form':form})
def change_password2(request):
    if request.method=='POST':
         form=SetPasswordForm(user=request.user,data=request.POST)
         if form.is_valid():
             form.save()
             update_session_auth_hash(request,form.user)
             return redirect('profile')
    else:
        form=SetPasswordForm(user=request.user)
    return render(request,'change_pass.html',{'form':form})