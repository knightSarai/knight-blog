from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail

from .models import Post
from .forms import EmailPostForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/list.html'


def posts_list(request):
    db_posts = Post.published.all()
    paginator = Paginator(db_posts, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

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


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Send mail
            form_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'Hello!, {form_data["name"]} recommends you read {post.title}'
            message = f'Read {post.title} at {post_url}\n\n {form_data["name"]}\'s comments: {form_data["comments"]}'
            send_mail(subject, message, 'mailknightsarai@gmail.com', [form_data['to']])
            sent = True

    else:
        form = EmailPostForm()

    return render(request, 'post/share.html', {
        'post': post,
        'form': form,
        'sent': sent
    })
