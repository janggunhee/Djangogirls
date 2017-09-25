from django.shortcuts import render

from .models import Post


def post_list(request):
    return render(request, 'blog/Post_list.html')


def post_list(request):
    posts = Post.objects.all()
    context = {
        # posts   key의 value는 QuerySet
        'post': posts,
    }
    return render(request, 'blog/post_list.html', context) # html 형태로 render