from django.db.models import Min
from rest_framework.exceptions import NotFound
from rest_framework import  status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response


from prefixes.models import IPv4prefix, IPv6prefix
#from prefixes.route_table import


IPv4table = None
IPv6table = None




class APIDestination(APIView):

    route_table = None

    def get(self, request, ip):
        print('here!')
        print(os.popen('pwd').read())

        '''
        c = 0
        for route in IPv4table:
            print(route)
            c += 1
            if c == 10:
                break
        '''
        best_path = self.route_table.search_best(ip)
        if best_path is None:
            raise NotFound
        content = {'prefix': best_path.prefix,
                   'nexthop': best_path.data['nexthop']}
        return Response(content, status=status.HTTP_200_OK)


class APIPrefixUpdate(APIView):

    model = None
    route_table = None

    def put(self, request):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(status.HTTP_404_NOT_FOUND)
        prefix = request.kwargs['prefix']
        metric = request.kwargs['metric']
        classifier = self.kwargs.get('classifier', 'orlonger')
        queryset.update(metric=metric)
        best_routes = self.get_best_routes(prefix, classifier)
        if len(updated_prefixes) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.update_route_table(best_routes)
        return Response(status=status.HTTP_200_OK)

    def get_queryset(self):
        prefix = self.kwargs['prefix']
        nexthop = self.kwargs['nexthop']
        classifier = self.kwargs.get('classifier', 'orlonger')
        if classifier == 'exact':
            return self.model.objects.filter(prefix=prefix,
                                             nexthop=nexthop)
        return self.model.objects.extra(
                where=['prefix <<= %s', 'nexthop = %s'],
                params=[prefix, nexthop]
            )

    def get_best_routes(self, prefix, classifier):
        if classifier == 'exact':
            return self.model.objects.values(
                'prefix'
            ).annotate(
                metric=Min('metric'),
                nexthop=Min('nexthop')
            ).filter(prefix=prefix).all()
        return self.model.objects.values(
            'prefix'
        ).annotate(
            metric=Min('metric'),
            nexthop=Min('nexthop')
        ).extra(where=['prefix <<= %s',], params=[prefix]).all()

    def update_route_table(self, best_routes):
        for route in best_routes:
            self.route_table.update(route['prefix'],
                                    route['nexthop'],
                                    route['metric'])


class APIDestinationIPv4(APIDestination):

    route_table = IPv4table


class APIDestinationIPv6(APIDestination):

    route_table = IPv6table

class APIPrefixIPv4(APIPrefixUpdate):

    model = IPv4prefix
    route_table = IPv4table

class APIPrefixIPv6(APIPrefixUpdate):

    model = IPv6prefix
    route_table = IPv6table


'''
prefix_list = [
    {'prefix':'10.0.0.0/16',
     'nexthop':'192.168.1.1',
     'metric': 300},
    {'prefix': '10.0.1.0/24',
     'nexthop': '192.168.2.1',
     'metric': 200},
    {'prefix': '10.0.2.0/24',
     'nexthop': '192.168.3.1',
     'metric': 400},
]

def load_all_prefixes(prefix_list):
    for prefix_object in prefix_list:
        node = table.add(prefix_object['prefix'])
        node.data['nexthop'] = prefix_object['nexthop']
        node.data['metric'] = prefix_object['metric']
        
@api_view(['PUT'])
def prefixes_bulk(request):
    IPv4prefix.objects.extra(
        where=['prefix <<= %s', 'nexthop = %s'],
        params=[prefix, nexthop]
    ).update(metric=metric)
    updated_prefixes = IPv4prefix.objects.extra(
        where=['prefix <<= %s', 'nexthop = %s'],
        params=[prefix, nexthop]
    ).all()
    for updated_prefix in updated_prefixes:
        IPv4table.update_prefix(updated_prefix.prefix,
                                updated_prefix.nexthop,
                                updated_prefix.metric)
'''

'''
@api_view(['GET'])
def destination(request, ip):
    #ip_address = request.kwargs['ip']
    best_path = IPv4table.search_best(ip)
    if best_path is None:
        raise NotFound
    content = {'prefix': best_path.prefix,
               'nexthop': best_path.data['nexthop']}
    return Response(content, status=status.HTTP_200_OK)

@api_view(['GET'])
def destination_v4(request, ip):
    destination(request, ip, IPv4table)

@api_view(['GET'])
def destination_v4(request, ip):
    destination(request, ip, IPv6table)
'''