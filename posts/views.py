from django.shortcuts import render, get_object_or_404, redirect, reverse
from promotions.models import Signup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from .models import Post, Author, PostView
from review.models import Review
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from .forms import CommentForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(
        Count('categories__title'))
    return queryset


def search(request):
    queryset = Post.objects.all()
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)
            | Q(overview__icontains=query)).distinct()

    context = {
        'queryset': queryset,
        'most_recent': most_recent,
        'category_count': category_count,
    }

    return render(request, 'search_results.html', context)


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    reviews = Review.objects.order_by('-date')[0:3]

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list': featured,
        'latest': latest,
        'reviews': reviews,
    }
    return render(request, 'index.html', context)


def blog(request):
    post_list = Post.objects.all()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    category_count = get_category_count()

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'most_recent': most_recent,
        'category_count': category_count,
    }
    return render(request, 'blog.html', context)

def post(request, id):
    post = get_object_or_404(Post, id=id)
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    form = CommentForm(request.POST or None)

    # if request.user.is_authenticated:
    #     PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={'id': post.pk}))
    context = {
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'form': form
    }

    return render(request, 'post.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form = CommentForm()

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk': post.pk
            }))


def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(
                reverse("post-detail", kwargs={'id': form.instance.id}))
    context = {'title': title, 'form': form}
    return render(request, "post_create.html", context)


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))



def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(
                reverse("post-detail", kwargs={'id': form.instance.id}))
    context = {'title': title, 'form': form}
    return render(request, "post_create.html", context)


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/blog'
    template_name = 'post_confirm_delete.html'



def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("post-list"))
