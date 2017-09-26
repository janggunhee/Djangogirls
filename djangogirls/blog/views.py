from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render

User = get_user_model() # user class 이다


from .models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        # posts key의 value는 QuerySet
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)

# View(Controller) 구현
# post_detail기능을 하는 함수를 구현
# 'post'라는 key로 Post.objects.first()에 해당하는 Post객체를 전달
# 템플릿은 'blog/post_detail.html'을 사용

def post_detail(request, pk):
    # Post인스턴스 1개만 가져옴, 변수명은 posts가 아닌 단일객체를 나타내는 post사용

    # get에 실패했을때 발생하는 예외
    #   Post.DoesNotExist
    # HTTP로 문자열을 돌려주려면
    #   HttpResponse
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse('No post', status=404)

    # 'post'key값으로 Post인스턴스 하나 전달
    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context)

def post_add(request):
    # post_form,html 에 checkbox를 추가
    # 이를 이용해서 publish여부를 결정
    #
    # Post 생성 완료 후 (DB에 저장 후, post list 페이지로 이동

    #

    if request.method == 'POST' and request.POST.get('title') and request.POST.get('content'):
        # request.POST(dict형 객체에서 title, 'content' 키에 해당하는 vaule 값을 받아
        # 새 Post 객체를 생성 (save() 호출없음 . 단순 인스턴스 생성
        # 생성한 후에는 해당 객체의 title, content를 HttpResponse
        # https://docs.djangoproject.com/ko/1.11/topics/http/shortcuts/#redirecrt


        # title이나 content값이 오지 않았을 경우에는 객체를 생성하지 않고 다시 작성 페이지로 이동
        title = request.POST['title']
        content = request.POST['content']
        author = User.objects.get(username='janggunhee')
        post = Post(
            author=author,
            title=title,
            content=content
        )
        post.publish()
        return HttpResponse(f'{post.title},{post.content}')
    else:
        context={

        }
        return render(request, 'blog/post_form.html', context)