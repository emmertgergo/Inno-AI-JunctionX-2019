from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.urls import reverse
from .forms import UserForm

# ============================================================================================
# User login and logout functions.
# ============================================================================================
@login_required
def user_logout(request):
    logout(request)
    if 'next'in request.GET:
        return HttpResponseRedirect(request.GET.get('next'))
    else:
        return render(request, 'children_app/list.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if request.POST.get('next') != '':
                    return HttpResponseRedirect(request.POST.get('next'))
                else:
                    return render(request, 'children_app/list.html')
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE!")
        else:
            print("LOGIN FAILED!")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request, 'userhandler_app/login.html', {})


# ============================================================================================
# Register a new user.
# ============================================================================================
def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request, 'userhandler_app/registration.html',
                          {'user_form': user_form,
                           'registered': registered})
