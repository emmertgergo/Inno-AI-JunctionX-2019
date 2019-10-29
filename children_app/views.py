from django.shortcuts import render
from .models import Child
from . import forms
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


class ChildList(LoginRequiredMixin, TemplateView):
    template_name = "children_app/list.html"

    def get_context_data(self, **kwargs):  # Ez a két sor itt ahhoz kell, hogy hozzáférjük a context-hez
        # amit belerakunka template-be
        context = super().get_context_data(**kwargs)
        all_child = Child.objects.filter(
            user=User.objects.get(pk=self.request.user.id)
        ).order_by('name')
        context['items'] = all_child
        return context


class AddChild(LoginRequiredMixin, TemplateView):
    template_name = 'children_app/add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.AddChild()
        return context

    def post(self, request, *args, **kwargs):

        form = forms.AddChild(request.POST, request.FILES)
        if form.is_valid():  # HA rendben van a form tartalma
            print("VALID FORM IN.")

            r1 = Child(
                    name=form.cleaned_data['name'],
                    image=form.cleaned_data['image'],
                    user=User.objects.get(pk=self.request.user.id),
                )
            r1.save()  # az osztály példányának mentésével írom az adatbázisba az adatokat
            return HttpResponseRedirect(reverse('children_app:child'))
        else:
            return render(request, 'children_app/add.html', {'form': form})


class SettingChild(LoginRequiredMixin, TemplateView):
    template_name = "children_app/setting.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        child = Child.objects.get(pk=kwargs['child_id'])
        settingform = forms.SettingsEmoji(instance=child)
        context['form'] = settingform
        return context

    def post(self, request, *args, **kwargs):
        form = forms.SettingsEmoji(request.POST, request.FILES)
        if form.is_valid():
            print("VALID FORM IN.")
            child = Child.objects.get(pk=kwargs['child_id'])
            child.emojitype = form.cleaned_data['emojitype']
            child.save()

            return HttpResponseRedirect(reverse('children_app:child'))




