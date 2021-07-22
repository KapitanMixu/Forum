from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.db.models import Q
# Create your views here.

from .models import Post, Comment, UserProfile
from .forms import CreateUserForm, CreatePost, CommentForm, RateForm, CustomAuthenticationForm


class IndexView(generic.ListView):
    template_name = 'forum/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        return Post.objects.order_by('-pub_date')[:30]


def DetailView(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.all()
    return render(request, 'forum/detail.html', {'post': post, 'comments': comments})


def ProfileView(request, up):
    userprofile = UserProfile.objects.get(pk=up)
    return render(request, 'forum/profile.html', {'userprofile': userprofile})


class MakingView(generic.CreateView):
    model = Post
    form_class = CreatePost
    template_name = 'forum/making.html'
    success_url = reverse_lazy('forum:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(MakingView, self).form_valid(form)


class RegisterPage(FormView):
    template_name = 'forum/register.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('forum:index')

    def form_valid(self, form):
        user = form.save()
        return super(RegisterPage, self).form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'forum/login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('forum:index')


class MakeComment(generic.CreateView):
    model = Comment
    template_name = 'forum/comment.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.main_post = Post(id=self.kwargs['pk'])
        return super(MakeComment, self).form_valid(form)

    def get_success_url(self):

        return reverse('forum:detail', kwargs={'pk': self.kwargs['pk']})


class UserProfileView(generic.DetailView):
    model = UserProfile
    template_name = 'forum/profile.html'


class SearchView(generic.ListView):
    model = Post
    template_name = 'forum/search.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(tags__icontains=query)
        )
        return object_list


def vote(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = RateForm(request.POST or None, initial={"rate": '5'})
    if request.method == 'POST':
        if form.is_valid():
            if form is None:
                a = 0
            else:
                a = int(form.cleaned_data['rate'])
            post.rate = round((post.rate*post.rate_number + a)/(post.rate_number + 1), 2)
            post.rate_number += 1
            post.save()
            return redirect('forum:detail', pk=pk)
    return render(request, 'forum/rating.html', {'form': form, 'post': post})

