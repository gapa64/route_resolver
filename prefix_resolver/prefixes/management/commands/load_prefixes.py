import re
from django.core.management.base import BaseCommand

from prefixes.models import IPv4prefix, IPv6prefix
from tools.regex_patterns import (IPv4_PATTERN, IPv6_PATTERN,
                                  IPv4_PREFIX_PATTERN, IPv6_PREFIX_PATTERN)

from datetime import datetime



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
        print('parsing start')
        now = datetime.now()
        with open(file_path) as raw_file:
            for row in raw_file:
                parsed_entry = self.IPv4_ROUTE_PATTERN.search(row)
                if parsed_entry is not None:
                    entry = self.create_object(parsed_entry, IPv4prefix)
                    ipv4_bulk.append(entry)
                    continue
                parsed_entry = self.IPv6_ROUTE_PATTERN.search(row)
                '''
                if parsed_entry is not None:
                    entry = self.create_object(parsed_entry, IPv6prefix)
                    ipv6_bulk.append(entry)
                    continue
                wrong_entries.append(row)
                '''
        print('parsing end', datetime.now() - now)
        print('bulk start')
        now = datetime.now()
        IPv4prefix.objects.bulk_create(ipv4_bulk)
        print('bulk end', datetime.now() - now)
        #IPv6prefix.objects.bulk_create(ipv6_bulk)
        for wrong in wrong_entries:
            print(wrong)

    def create_object(self, parsed_entry, model):
        prefix = parsed_entry.group('prefix')
        nexthop = parsed_entry.group('nexthop')
        return model(prefix=prefix, nexthop=nexthop)


'''   
        parsed_data = self.get_json_from_file(file_path)
        bulk, inconsistents, duplicates = self.prepare_bulk_create(
            parsed_data
        )
        Ingredient.objects.bulk_create(bulk)
        if len(inconsistents) >= 1:
            self.report_issue(inconsistents)
        if len(duplicates) >= 1:
            self.report_duplicates(duplicates)
'''
