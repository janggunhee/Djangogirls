from django.shortcuts import render

from .models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        # posts key의 value는 QuerySet
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)