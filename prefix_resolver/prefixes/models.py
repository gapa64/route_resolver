from django.db import models

from .validators import metric_validator

class BasePrefix(models.Model):
    prefix = models.GenericIPAddressField()
    nexthop = models.GenericIPAddressField()
    metric = models.IntegerField(
        default=100,
        validators=[metric_validator]
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['prefix', 'nexthop'],
                                    name='unique_prefix_nexthop')
        ]

    def __str__(self) -> str:
        return f'{self.prefix}_{self.nexthop}'

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['prefix']),
        ]


class IPv4prefix(BasePrefix):
    pass

class IPv6prefix(BasePrefix):
    pass
