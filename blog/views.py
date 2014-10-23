from django.shortcuts import render, get_object_or_404
from blog.models import Post, Tag


# def home(request):
#     return render(request, 'home.html', {
#         'latest_post': Post.objects.latest('created')
#         'latest_post': Post.objects.order_by('-created')[0]
#     })


def blog(request):
    # print request.location

    return render(request, 'blog.html', {
        'posts': Post.objects.order_by('-created')
    })


def post(request, pk):
    post_obj = get_object_or_404(Post, pk=pk)

    return render(request, 'post.html', {
        'post': post_obj
    })

def tag(request, pk):
    tag_obj = get_object_or_404(Tag, pk=pk)

    return render(request, 'blog.html', {
        'posts': tag_obj.posts.all(), 'tags': tag_obj
    })


def error(request):
    my_variable = '!'
    my_list = ['testing', 'a', 'list', 'out']
    my_list = ["{}{}".format(list_item, my_variable) for list_item in my_list]
    raise NotImplementedError("Woops! This doesn't exist.")