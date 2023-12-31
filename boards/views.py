from django.db.models import Count
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView

from .forms import NewTopicForm, PostForm
from .models import Board, Topic, Post

User = get_user_model()

class BoardListView(ListView):
    template_name = 'home.html'
    model = Board
    context_object_name = 'boards'

class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, slug=self.kwargs.get('slug'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset

class BoardCreateView(UserPassesTestMixin, CreateView):
    model = Board
    template_name = 'board_create.html'
    fields = ('name', 'description')
    success_url = reverse_lazy('home')
    
    def test_func(self):
        return self.request.user.is_staff

@login_required    
def new_topic(request, slug):
    board = get_object_or_404(Board, slug=slug)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic = topic,
                created_by = request.user
            )
            return redirect('topic_posts', slug=slug, topic_id=topic.id)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})
    
class PostListView(ListView):
    model = Post
    template_name = 'topic_posts.html'
    context_object_name = 'posts'
    paginate_by = 2
    
    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__slug=self.kwargs.get('slug'), pk=self.kwargs.get('topic_id'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

@login_required 
def reply_topic(request, slug, topic_id):
    topic = get_object_or_404(Topic, board__slug=slug, id=topic_id)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            
            topic.last_updated = timezone.now()
            topic.save()
            
            topic_url = reverse("topic_posts", kwargs={"slug": slug, "topic_id": topic_id})
            topic_post_url = "{url}?page={page}#{id}".format(url=topic_url, page=topic.get_page_count(), id=post.id)
            
            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, "reply_topic.html", {'topic': topic, 'form': form})

@method_decorator(login_required, name="dispatch")
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'
    success_url = reverse_lazy('my_account')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect("topic_posts", slug=post.topic.board.slug, topic_id=post.topic.id)


    
    
    