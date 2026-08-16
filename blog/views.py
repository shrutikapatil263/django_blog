from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Post


def post_list(request):
    """Display a paginated list of all blog posts, most recent first."""
    post_queryset = Post.objects.select_related('author').all()

    paginator = Paginator(post_queryset, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """Show a single post, its comments, and a form to add a new comment."""
    post = get_object_or_404(Post.objects.select_related('author'), slug=slug)
    comments = post.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment has been posted.')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_create(request):
    """Handle the creation of a new blog post. Requires an authenticated user."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been published!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()

    context = {'form': form}
    return render(request, 'blog/post_form.html', context)
