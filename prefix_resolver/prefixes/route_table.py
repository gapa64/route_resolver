from django.db.models import Min
from ipaddress import IPv4Address, IPv6Address
import pickle
import radix

from .models import IPv4prefix, IPv6prefix
from datetime import datetime

class RouteTableError(BaseException):
    pass

class RouteTable(radix.Radix):

    IP_CONVERTER = {
        'v4': IPv4Address,
        'v6': IPv6Address,
    }
    def __init__(self, family):
        if family not in self.IP_CONVERTER:
            raise RouteTableError('Unsuported family')
        self.family = family
        super().__init__()

    def add_prefix(self, prefix, nexthop, metric=100):
        node = self.add(prefix)
        node.data['nexthop'] = self.IP_CONVERTER[self.family](nexthop)
        node.data['metric'] = metric

    def update_prefix(self, prefix, nexthop, metric=100):
        current_prefix = self.search_exact(prefix)
        if current_prefix is None:
            self.add_prefix(prefix, nexthop, metric)
            return
        candidate_nexthop = self.IP_CONVERTER[self.family](nexthop)
        new_nexthop, new_metric = self.compare_prefixes(
            existent_nexthop=current_prefix.data['nexthop'],
            existent_metric=current_prefix.data['metric'],
            candidate_nexthop=candidate_nexthop,
            candidate_metric=metric)
        current_prefix.data[nexthop] = new_nexthop
        current_prefix.data[new_metric] = new_metric

    @staticmethod
    def compare_prefixes(existent_nexthop, existent_metric,
                         candidate_nexthop, candidate_metric):
        if candidate_metric < existent_metric:
            return candidate_nexthop, candidate_metric
        elif candidate_metric == existent_metric:
            if candidate_nexthop < existent_nexthop:
                return candidate_nexthop, candidate_metric
        return existent_nexthop, existent_metric

#class RouteTableLauncher:



def init_route_table(table, model):
    print('grabing prefs')
    now = datetime.now()
    best_prefixes = model.objects.values(
        'prefix'
    ).annotate(metric=Min('metric'), nexthop=Min('nexthop')).all()
    print('sql done',  datetime.now() - now)
    print('updating radix')
    now = datetime.now()
    for prefix_dict in best_prefixes:
        prefix = prefix_dict['prefix']
        nexthop = prefix_dict['nexthop']
        metric = prefix_dict['metric']
        table.add_prefix(prefix, nexthop, metric)
    print('radix done', datetime.now() - now)
    print('pickling start')
    now = datetime.now()
    serialize_route_table(table, 'cache')
    print('Pickling done', datetime.now() - now)


def serialize_route_table(route_table, file):
    with open(file, 'wb') as fl_obj:
        pickle.dump(route_table, fl_obj)

def deserialize_route_table(route_table, file):
    with open(file, 'wb') as fl_obj:
        return pickle.load(route_table, fl_obj)





'''
class RouteTable(radix.Radix):

    #def __init__(self, family):
    #    self.family = family

    def add_prefix(self, prefix, nexthop, metric=100):
        node = self.add(prefix)
        node.data['nexthop'] = nexthop
        node.data['metric'] = metric

    def update_prefix(self, prefix, nexthop, metric=100):
        current_prefix = self.search_exact(prefix)
        if current_prefix is None:
            self.add_prefix(prefix, nexthop, metric)
        new_nexthop, new_metric = self.compare_prefixes(
            existent_nexthop=current_prefix.data['nexthop'],
            existent_metric=current_prefix.data['metric'],
            candidate_nexthop=nexthop,
            candidate_metric=metric)
        current_prefix.data[nexthop] = new_nexthop
        current_prefix.data[new_metric] = new_metric

    @staticmethod
    def compare_prefixes(existent_nexthop, existent_metric,
                         candidate_nexthop, candidate_metric, family='V4'):
        if candidate_metric < existent_metric:
            return candidate_nexthop, candidate_metric
        elif candidate_metric == existent_metric:
            if family == 'V4':
                existent_ip = IPv4Address(existent_nexthop)
                candidate_ip = IPv4Address(candidate_nexthop)
            else:
                existent_ip = IPv6Address(existent_nexthop)
                candidate_ip = IPv6Address(candidate_nexthop)
            if candidate_ip < existent_ip:
                return candidate_nexthop, candidate_metric
        return existent_nexthop, existent_metric

def init_route_table(table, model):
    best_prefixes = model.objects.values(
        'prefix'
    ).annotate(metric=Min('metric'), nexthop=Min('nexthop')).all()
    for prefix_dict in best_prefixes:
        prefix = prefix_dict['prefix']
        nexthop = prefix_dict['nexthop']
        metric = prefix_dict[metric]
        table.add_prefix(prefix, nexthop, metric)

print(__name__)
'''
IPv4table = RouteTable('v4')
IPv6table = RouteTable('v6')
#init_route_table(IPv4table, IPv4prefix)
#init_route_table(IPv6table, IPv6prefix)
