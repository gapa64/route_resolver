from django.urls import re_path, path

from .views import (APIDestinationIPv4, APIDestinationIPv6,
                    APIPrefixIPv4, APIPrefixIPv6)
from tools.regex_patterns import (IPv4_PATTERN, IPv6_PATTERN,
                                  IPv4_WEB_PREFIX_PATTERN,
                                  IPv6_WEB_PREFIX_PATTERN)

ipv4_prefix_url = (
    rf'prefix/(?P<prefix>{IPv4_WEB_PREFIX_PATTERN})'
    rf'/nh/(?P<nexhhop>{IPv4_PATTERN})/'
    rf'metric/(?P<metric>\d+)'
    rf'(/match/(?P<classifier>orlonger|exact))?'
)
ipv6_prefix_url = (
    rf'prefix/(?P<prefix>{IPv6_WEB_PREFIX_PATTERN})'
    rf'/nh/(?P<nexhhop>{IPv6_PATTERN})/'
    rf'metric/(?P<metric>\d+)'
    rf'(/match/(?P<classifier>orlonger|exact))?'
)

urlpatterns = [
    re_path(rf'destination/(?P<ip>{IPv4_PATTERN})',
            APIDestinationIPv4.as_view(),
            name='destination_ipv4'),
    re_path(rf'destination/(?P<ip>{IPv6_PATTERN})',
            APIDestinationIPv6.as_view(),
            name='destination_ipv6'),
    re_path(ipv4_prefix_url,
            APIPrefixIPv4.as_view(),
            name='prefix_ipv4'),
    re_path(ipv6_prefix_url,
            APIPrefixIPv6.as_view(),
            name='prefix_ipv6')
]



'''
router.register('titles', TitleViewSet, basename='title')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
urlpatterns = [
    re_path(rf'destination/(?P<ip>({IPv4_PATTERN}|{IPv6_PATTERN}))',
            destination,
            name='ip_destination'),
]
)
'''