from blog.models import Post, Tag


def latest_post(request):
    return {
        'latest_post': Post.objects.latest('created')
    }


def list_tags(request):
    return {
        'list_tags': Tag.objects.all()
    }