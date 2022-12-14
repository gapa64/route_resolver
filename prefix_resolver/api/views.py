
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from prefixes.models import IPv4prefix, IPv6prefix


class APIDestination(APIView):

    model = None

    def get(self, request, ip):
        best_path = self.model.objects.extra(
            where=['prefix >>= %s'],
            params=[ip]
        ).order_by('-prefix', 'metric', 'nexthop').first()
        if best_path is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        content = {'dst': best_path.prefix,
                   'nh': best_path.nexthop}
        return Response(content, status=status.HTTP_200_OK)


class APIPrefixUpdate(APIView):

    model = None
    route_table = None

    def put(self, request, prefix, nexthop,
            metric, classifier=None):
        print(request, prefix, nexthop)
        queryset = self.get_queryset(prefix,
                                     nexthop,
                                     classifier)
        if not queryset.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        queryset.update(metric=metric)
        return Response(status=status.HTTP_200_OK)

    def get_queryset(self, prefix, nexthop, classifier):
        if classifier == 'exact':
            return self.model.objects.filter(prefix=prefix,
                                             nexthop=nexthop)
        return self.model.objects.extra(
                where=['prefix <<= %s', 'nexthop = %s'],
                params=[prefix, nexthop]
            )


class APIDestinationIPv4(APIDestination):

    model = IPv4prefix


class APIDestinationIPv6(APIDestination):

    model = IPv6prefix


class APIPrefixIPv4(APIPrefixUpdate):

    model = IPv4prefix


class APIPrefixIPv6(APIPrefixUpdate):

    model = IPv6prefix
