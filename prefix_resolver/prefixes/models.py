from django.db import models

from .validators import metric_validator


class BasePrefix(models.Model):
    prefix = models.GenericIPAddressField()
    nexthop = models.GenericIPAddressField()
    metric = models.IntegerField(
        default=1000,
        validators=[metric_validator]
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(fields=['prefix', 'nexthop'],
                                    name='unique_prefix_nexthop')
        ]

    def __str__(self) -> str:
        return f'{self.prefix}_{self.nexthop}'

class IPv4prefix(BasePrefix):

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['prefix', 'nexthop'],
                                    name='unique_v4_prefix_nexthop')
            ]


class IPv6prefix(BasePrefix):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['prefix', 'nexthop'],
                                    name='unique_v6_prefix_nexthop')
        ]


