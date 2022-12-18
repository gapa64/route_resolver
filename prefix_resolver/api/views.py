
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from prefixes.models import IPv4prefix, IPv6prefix
from .serializers import (IPv4DestinationSerializer,
                          IPv6DestinationSerializer)


class APIDestination(APIView):

    model = None
    serializer = None

    def get(self, request, ip):
        best_path = self.model.objects.extra(
            where=['prefix >>= %s'],
            params=[ip]
        ).order_by('-prefix', 'metric', 'nexthop').first()
        if best_path is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        destination_serializer = self.serializer(best_path)
        return Response(destination_serializer.data,
                        status=status.HTTP_200_OK)


class APIPrefixUpdate(APIView):

    model = None

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
    serializer = IPv4DestinationSerializer


class APIDestinationIPv6(APIDestination):

    model = IPv6prefix
    serializer = IPv6DestinationSerializer


class APIPrefixIPv4(APIPrefixUpdate):

    model = IPv4prefix


class APIPrefixIPv6(APIPrefixUpdate):

    model = IPv6prefix
