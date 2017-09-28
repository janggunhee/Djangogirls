from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Post

User = get_user_model() # user class 이다


def post_list(request):
    # post_list view가 published_date가 존재하는 Post목록만 보여주도록 수정
    posts = Post.objects.filter(published_date__isnull=False)
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
    # post_list.html에 post_add로 갈 수 있는 버튼링크 추가 ({% url %}태그 사용해서 동적으로 구성)
    #
    # post_form.html에 checkbox를 추가
    #   이를 이용해서 publish여부를 결정
    #
    # Post생성 완료 후(DB에 저장 후), post_list페이지로 이동
    #   https://docs.djangoproject.com/ko/1.11/topics/http/shortcuts/#redirect
    #    extra) 작성한 Post에 해당하는 post_detail페이지로 이동
    #
    # Post생성시 Post.objects.create()메서드 사용
    #
    # extra) Post delete기능 구현
    #   def post_delete(request, pk):
    #       (POST요청에서만 동작해야함)
    #       -> pk에 해당하는 Post를 삭제하고, post_list페이지로 이동

    # title이나 content중 하나만 왔을 경우,
    # 다시 입력페이지로 돌아가지만 채웠던 내용은 남도록 처리
    #   1. 아래 두 내용을 변수로 할당
    #     request.POST.get('title')
    #     request.POST.get('content')
    #   2. 둘 중 하나만 있을 경우를 if문의 조건으로 할당
    #   3. 변수로 할당한 위 값들을 context를 이용해 넘겨줌 <- render()
    #       if POST:
    #           Only POST process
    #           if valid POST request:
    #               return redirect()
    #       else:
    #           Only GET process
    #       return render()
    #   4. 템플릿에서는 context에 위 변수들이 올 경우 input들의 'value'속성 값으로 할당
    #       textarea는 내용을 채움
    #           <input value="내용">
    #           <textarea>실제내용</textarea>
    if request.method == 'POST':
        # request.POST(dict형 객체)에서 'title', 'content'키에 해당하는 value를 받아
        # 새 Post객체를 생성 (save() 호출없음. 단순 인스턴스 생성)
        # 생성한 후에는 해당 객체의 title, content를 HttpResponse로 전달

        # title이나 content값이 오지 않았을 경우에는 객체를 생성하지 않고 다시 작성페이지로 이동 (render또는 redirect)
        #   extra) 작성페이지로 이동 시 '값을 입력해주세요'라는 텍스트를 어딘가에 표시 (render)
        #   extra*****) Bootstrap을 사용해서 modal띄우기
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_publish = bool(request.POST.get('is_publish'))
        author = User.objects.get(username='lhy')

        # title과 content가 모두 전달되었을때만 Post생성
        if title and content:
            post = Post.objects.create(
                author=author,
                title=title,
                content=content,
            )
            if is_publish:
                post.publish()
            else:
                post.save()
            return redirect('post_detail', pk=post.pk)

        context = {
            'title': title,
            'content': content,
        }
    else:
        context = {}

    return render(request, 'blog/post_form.html', context)


def post_delete(request, pk):
    """
    pk에 해당하는 Post객체를 DB에서 삭제 (QuerySet.delete() 또는 Model.delete() 메서드 사용)
    1. post = 해당 Post객체를 할당
    2. post객체를 DB에서 삭제
    3. post_list로 redirect
    4. urls.py에 연결
        ex) /posts/3/delete/
    5. POST method로 요청시에만 작업을 처리
    :param request:
    :param pk: Post의 pk
    :return: redirect('post_list')
    """
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('post_list')
    return HttpResponse('Permission denied', status=403)


