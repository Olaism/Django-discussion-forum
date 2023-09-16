from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

from .forms import NewTopicForm
from .models import Board, Topic, Post

User = get_user_model()

def home(request):
    boards = Board.objects.all()
    
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    
    return render(request, 'topics.html', {'board': board})
    
    
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()
    print(user)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic = topic,
                created_by = user
            )
            return redirect('board_topics', pk=board.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})