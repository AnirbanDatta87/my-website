from django.shortcuts import render
from .models import Project
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# def project_list(request):
#     context = {
#         'projects': Project.objects.all()
#     }
#     return render(request, 'projects/project_list.html', context)

class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'


class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'project'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    context_object_name = 'project'
    fields = ['title', 'category', 'thumbnail', 'tagline', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    context_object_name = 'project'
    fields = ['title', 'category', 'thumbnail', 'tagline', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.author:
            return True
        return False


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    context_object_name = 'project'
    success_url = '/projects/'

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.author:
            return True
        return False
