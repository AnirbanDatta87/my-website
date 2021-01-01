from django.shortcuts import render
from .models import Review
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

class ReviewListView(ListView):
    model = Review
    context_object_name = 'reviews'


class ReviewDetailView(DetailView):
    model = Review
    context_object_name = 'review'


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    context_object_name = 'review'
    fields = ['title', 'category', 'thumbnail', 'tagline', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    context_object_name = 'review'
    fields = ['title', 'category', 'thumbnail', 'tagline', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.author:
            return True
        return False


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    context_object_name = 'review'
    success_url = '/reviews/'

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.author:
            return True
        return False
