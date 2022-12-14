import re
from django.core.management.base import BaseCommand

from prefixes.models import IPv4prefix, IPv6prefix
from tools.regex_patterns import (IPv4_PATTERN, IPv6_PATTERN,
                                  IPv4_PREFIX_PATTERN, IPv6_PREFIX_PATTERN)


class Command(BaseCommand):

    IPv4_ROUTE_PATTERN = re.compile(rf'(?P<prefix>{IPv4_PREFIX_PATTERN});'
                                    rf'(?P<nexthop>{IPv4_PATTERN})')
    IPv6_ROUTE_PATTERN = re.compile(rf'(?P<prefix>{IPv6_PREFIX_PATTERN});'
                                    rf'(?P<nexthop>{IPv6_PATTERN})')

    FAMILIES = {'v4': {'pattern': IPv4_ROUTE_PATTERN,
                       'model': IPv4prefix},
                'v6': {'pattern': IPv6_ROUTE_PATTERN,
                       'model': IPv6prefix}}

    def add_arguments(self, parser):
        parser.add_argument('file_path',
                            type=str,
                            help='specify file to load')

    def handle(self, *args, chunk_size=100, **kwargs):
        bulks = {'v4': [],
                 'v6': []}
        file_path = kwargs['file_path']
        with open(file_path) as raw_file:
            for row in raw_file:
                for family, data in self.FAMILIES.items():
                    parsed_entry = data['pattern'].search(row)
                    if parsed_entry is None:
                        continue
                    entry = self.create_object(parsed_entry,
                                               data['model'])
                    bulks[family].append(entry)
                    if len(bulks[family]) < chunk_size:
                        continue
                    data['model'].objects.bulk_create(bulks[family])
                    bulks[family] = []

    def create_object(self, parsed_entry, model):
        prefix = parsed_entry.group('prefix')
        nexthop = parsed_entry.group('nexthop')
        return model(prefix=prefix, nexthop=nexthop)
