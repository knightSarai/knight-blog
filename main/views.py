from django.shortcuts import render, get_object_or_404
from .models import Post


def posts_list(request):
    posts = Post.published.all()
    return render(request, 'post/list.html', {'posts': posts})


def get_post(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'post/detail.html',
                  {'post': post})
