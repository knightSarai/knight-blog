from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count
from taggit.models import Tag

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/list.html'


def posts_list(request, tag_slug=None):
    db_posts = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        db_posts = db_posts.filter(tags__in=[tag])

    paginator = Paginator(db_posts, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'page': page_number,
        'posts': posts,
        'tag': tag
    }

    return render(request, 'post/list.html', context)


def get_post(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    comments = post.comments.filter(active=True)
    new_comment = None
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published \
        .filter(tags__in=post_tags_ids) \
        .exclude(id=post.id) \
        .annotate(shared_tags=Count('tags')) \
        .order_by('-shared_tags', '-publish')[:4]

    if request.method == 'POST':
        # Create new comment
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts
    }
    return render(request, 'post/detail.html', context)


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
