from django.core.management.base import BaseCommand

from prefixes.models import IPv4prefix, IPv6prefix
from prefixes.route_table import init_route_table, IPv4table, IPv6table


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        init_route_table(IPv4table, IPv4prefix)
        #init_route_table(IPv6prefix, IPv6table)
