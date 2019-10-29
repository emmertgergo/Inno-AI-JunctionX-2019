from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


# ============================================================================================
# Index page.
# ============================================================================================
def index(request):
    return render(request, 'basic_app/index.html')


def login(request):
    return render(request, 'userhandler_app/login.html')
