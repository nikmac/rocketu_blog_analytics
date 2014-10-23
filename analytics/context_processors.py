from analytics.models import Advertisement


def location(request):
    return {
        'location': request.location
    }

def advertisement(request):
    return {
        'advertisements': Advertisement.objects.all()
    }

def random(request):
    return {
        'random_ad': Advertisement.objects.order_by('state', '?')
    }