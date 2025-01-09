from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    # Fetch all posts from the database, ordered by creation date
    posts = Post.objects.all().order_by('-created_at')
    # Render the 'post_list.html' template and pass the posts context
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, slug):
    # Fetch a single post based on the slug, or return a 404 if not found
    post = get_object_or_404(Post, slug=slug)
    # Render the 'post_detail.html' template and pass the single post context
    return render(request, 'blog/post_detail.html', {'post': post})
