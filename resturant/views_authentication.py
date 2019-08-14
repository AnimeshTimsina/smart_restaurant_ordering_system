from django.shortcuts import render,redirect
from django.contrib.auth import login, get_user_model, logout,update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import editProfileForm
from .models import Profile

# Create your views here.

@login_required
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!.LogIn again')
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@login_required
def view_profile(request):
    user = request.user
    args = {'user': user}
    return render(request, 'management/profile.html', args)

@login_required
def editProfile(request,key):
    p = Profile.objects.get(pk = key)
    if request.method=='POST':
        form = editProfileForm(request.POST,instance=p)
        if form.is_valid:
            form.save()
            messages.success(request, f'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.warning(request, f'Invalid input')
    else:
        form = editProfileForm(instance=p)
    args = {'form':form}
    return render(request,'management/editProfile.html',args)

@login_required
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("{% url 'profile' %}")
        else:
            return redirect("{% url 'changePassword' %}")
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)
