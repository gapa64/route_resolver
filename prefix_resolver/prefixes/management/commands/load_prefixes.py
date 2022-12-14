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

    def add_arguments(self, parser):
        parser.add_argument('file_path',
                            type=str,
                            help='specify file to load')


    def handle(self, *args, **kwargs):
        ipv4_bulk = []
        ipv6_bulk = []
        wrong_entries = []
        file_path = kwargs['file_path']
        with open(file_path) as raw_file:
            for row in raw_file:
                parsed_entry = self.IPv4_ROUTE_PATTERN.search(row)
                if parsed_entry is not None:
                    v4_entry = self.create_object(parsed_entry, IPv4prefix)
                    ipv4_bulk.append(v4_entry)
                    continue
                parsed_entry = self.IPv6_ROUTE_PATTERN.search(row)
                if parsed_entry is not None:
                    v6_entry = self.create_object(parsed_entry, IPv6prefix)
                    ipv6_bulk.append(v6_entry)
                    continue
                wrong_entries.append(row)
        IPv4prefix.objects.bulk_create(ipv4_bulk)
        IPv6prefix.objects.bulk_create(ipv6_bulk)
        if len(wrong_entries) != 0:
            self.print_wrong(wrong_entries)


    def create_object(self, parsed_entry, model):
        prefix = parsed_entry.group('prefix')
        nexthop = parsed_entry.group('nexthop')
        return model(prefix=prefix, nexthop=nexthop)

    def print_wrong(self, wrong_entries):
        print('The following entriees not loaded int DB')
        for wrong in wrong_entries:
            print(wrong)
