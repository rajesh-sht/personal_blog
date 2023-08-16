from django.shortcuts import render, HttpResponseRedirect, redirect
from blog_app.models import Post
from blog_app.forms import PostForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def post_list(request):
    posts = Post.objects.filter(
        published_at__isnull=False).order_by('-published_at')
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, id):
    post = Post.objects.get(pk=id)
    return render(request, 'post_detail.html', {"post": post})


@login_required
def post_delete(request, id):
    post = Post.objects.get(pk=id)
    post.delete()
    return HttpResponseRedirect('/')


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            author = request.user
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            Post.objects.create(title=title, content=content, author=author)
            return redirect('draft-list')
    else:
        form = PostForm()
        return render(request, 'post_create.html', {'form': form})


@login_required
def post_edit(request, id):
    post = Post.objects.get(pk=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            author = request.user
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            Post.objects.create(title=title, content=content, author=author)
            return HttpResponseRedirect('/')
    else:
        form = PostForm(instance=post)
        return render(request, 'post_create.html', {'form': form})


@login_required
def draft_list(request):
    posts = Post.objects.filter(published_at__isnull=True)
    return render(request, 'draft_list.html', {'posts': posts})


@login_required
def post_publish(request, id):
    post = Post.objects.get(pk=id)
    post.published_at = timezone.now()
    post.save()
    return redirect('post-list')
