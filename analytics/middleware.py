from django.conf import settings
import requests
from ipware.ip import get_real_ip
from analytics.models import Page, Location, View


class LocationMiddleware(object):
    def process_request(self, request):
        # Get the IP Address of this request
        ip = get_real_ip(request)

        # If we didn't get an IP Address and we're developing locally,
        # make an API call to get our IP Address.
        if ip is None and settings.DEBUG:
            ip = requests.get('http://icanhazip.com/').text

        if ip is not None:
            response = requests.get('http://ipinfo.io/{}/json'.format(ip))
            if response.status_code == 200:
                request.location = response.json()
                # Split out the lat and long from the location
                request.location['latitude'], request.location['longitude'] = request.location['loc'].split(',')

        request.ip = ip


class PageViewMiddleware(object):
    def process_request(self, request):
         #TODO: get or create the Page object
         #TODO: get the URL - request.META['PATH_INFO']
         #'page, created' and 'location, created' sets the tuple
        page, created = Page.objects.get_or_create(url=request.META.get('PATH_INFO'))
        #TODO: Get or create the Location object
         #TODO: get info from request.location
        location = latitude = longitude = None
        if request.location:
            location, created = Location.objects.get_or_create(city=request.location['city'],
                                                               region=request.location['region'],
                                                               country=request.location['country'])
            latitude = request.location['latitude']
            longitude = request.location['longitude']
        #TODO: Create the View object
        View.objects.create(page=page, location=location, latitude=latitude, longitude=longitude,
                            ip_address=request.ip)


