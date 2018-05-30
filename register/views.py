from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from . models import ProjectType, Tier
from . forms import ProjectTypeForm, TierForm


class ProjectTypeDelete(DeleteView):
    model = ProjectType
    success_url = reverse_lazy("register:projecttype_list")


class ProjectTypeUpdate(UpdateView):
    model = ProjectType
    form_class = ProjectTypeForm
    template_name_suffix = "_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = ProjectType.objects.all()
        context['existing_objects'] = existing_objects
        return context


class ProjectTypeDetail(DetailView):
    model = ProjectType
    form_class = ProjectTypeForm


class ProjectTypeList(ListView):
    model = ProjectType


class ProjectTypeCreate(CreateView):
    model = ProjectType
    template_name_suffix = "_create"
    form_class = ProjectTypeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = ProjectType.objects.all()
        context['existing_objects'] = existing_objects
        return context


class TierCreate(CreateView):
    model = Tier
    template_name_suffix = "_create"
    form_class = TierForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Tier.objects.all()
        context['existing_objects'] = existing_objects
        return context


class TierList(ListView):
    model = Tier


class TierDetail(DetailView):
    model = Tier


class TierDelete(DeleteView):
    model = Tier
    success_url = reverse_lazy("register:tier_list")


class TierUpdate(UpdateView):
    model = Tier
    form_class = TierForm
    template_name_suffix = "_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Tier.objects.all()
        context['existing_objects'] = existing_objects
        return context
