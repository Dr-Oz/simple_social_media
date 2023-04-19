from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import PostForm, CommentForm
from .models import Post, Group, User, Follow
from django.urls import reverse

from .pagination import CatsPagination
from .serializers import PostSerializer, GroupSerializer, UserSerializer
from .permissions import AuthorOrReadOnly, ReadOnly
from .throttling import WorkingHoursRateThrottle
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    # Если порядок сортировки определен в классе Meta модели,
    # запрос будет выглядить так:
    # post_list = Post.objects.all()
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, 3)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'post/index.html', context)


# View-функция для страницы сообщества:
def group_posts(request, slug):
    # Функция get_object_or_404 получает по заданным критериям объект
    # из базы данных или возвращает сообщение об ошибке, если объект не найден.
    # В нашем случае в переменную group будут переданы объекты модели Group,
    # поле slug у которых соответствует значению slug в запросе
    group = get_object_or_404(Group, slug=slug)

    # Метод .filter позволяет ограничить поиск по критериям.
    # Это аналог добавления
    # условия WHERE group_id = {group_id}
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'post/group_list.html', context)


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    user = User.objects.get(username=username)
    post_user = Post.objects.filter(author=user).order_by('-pub_date')
    post_one = Post.objects.filter(author=user).order_by('-pub_date')[:1]
    paginator = Paginator(post_user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user, author=user
        ).exists()
    else:
        following = False
    context = {
        'username': username,
        'page_obj': page_obj,
        'post_user': post_user,
        'post_one': post_one,
        'following': following,
    }
    return render(request, 'post/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = post.author
    comment_form = CommentForm()
    post_user = Post.objects.filter(author=user).order_by('-pub_date')
    context = {
        'post': post,
        'post_user': post_user,
        'comment_form': comment_form
    }
    return render(request, 'post/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        id = request.user.id
        author_id = User.objects.get(id=id)
        username = request.user.username
        form = PostForm(
            request.POST or None,
            files=request.FILES or None,)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = author_id
            post.save()
            return redirect('post_app:profile', username)

    form = PostForm()
    context = {
        "form": form,
    }
    return render(request, 'post/create_post.html', context)


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(
            request.POST or None,
            files=request.FILES or None,
            instance=post
        )
        if form.is_valid():
            form.save()
        return redirect('post_app:post_detail', post_id=post.id)

    form = PostForm(instance=post)
    return render(request, 'post/create_post.html', {'form': form, 'post': post})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    id = request.user.id
    author_id = User.objects.get(id=id)
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            new_comment.author = author_id
            # Save the comment to the database
            new_comment.save()
        else:
            comment_form = CommentForm()
        return render(request,
                      'post/post_detail.html',
                      {'post': post,
                       'comments': comments,
                       'comment_form': comment_form})

@login_required
def follow_index(request):
    list_of_posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(list_of_posts, 20)
    page_namber = request.GET.get('page')
    page = paginator.get_page(page_namber)
    context = {'page': page}
    return render(request, 'post/follow.html', context)


@login_required
def profile_follow(request, username):
    user = request.user
    author = User.objects.get(username=username)
    is_follower = Follow.objects.filter(user=user, author=author)
    if user != author and not is_follower.exists():
        Follow.objects.create(user=user, author=author)
    return redirect(reverse('post_app:profile', args=[username]))


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    is_follower = Follow.objects.filter(user=request.user, author=author)
    if is_follower.exists():
        is_follower.delete()
    return redirect('post_app:profile', username=author)

@api_view(['GET', 'POST'])
def api_post(request):
    if request.method == 'GET':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_posts_detail(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = PostSerializer(post)
    return Response(serializer.data)

# class APIPost(APIView):
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class APIPostDetail(APIView):
#     def get(self, request, pk):
#         post = Post.objects.get(pk=pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def delete(self, request, pk):
#         post = Post.objects.get(pk=pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def put(self, request, pk):
#         post = Post.objects.get(pk=pk)
#         serializer = PostSerializer(post, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, pk):
#         post = Post.objects.get(pk=pk)
#         serializer = PostSerializer(post, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class APIPostList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#
# class APIPostDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)
    throttle_classes = (WorkingHoursRateThrottle, )
    #pagination_class = CatsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = None
    filtered_fields = ('author', 'group')
    search_fields = ('$text',)
    ordering_fields = ('author', 'group')
    ordering = ('group',)
    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернем обновленный перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()
    def get_queryset(self):
        queryset = Post.objects.all()
        group = self.request.query_params.get('group')
        if group is not None:
            queryset = queryset.filter(group=group)
        return queryset

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer