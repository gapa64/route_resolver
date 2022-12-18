from rest_framework import serializers

from prefixes.models import IPv4prefix, IPv6prefix, BasePrefix


class DestinationSerializer(serializers.ModelSerializer):

    dst = serializers.IPAddressField(source='prefix')
    nh = serializers.IPAddressField(source='nexthop')

    class Meta:
        model = BasePrefix
        fields = '__all__'


class IPv4DestinationSerializer(DestinationSerializer):

    class Meta:
        model = IPv4prefix
        fields = ('dst',
                  'nh')

class IPv6DestinationSerializer(DestinationSerializer):

    class Meta:
        model = IPv6prefix
        fields = ('dst',
                  'nh')
