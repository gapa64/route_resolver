from rest_framework.exceptions import ValidationError

def metric_validator(value):
    if not 1 <= value <= 32768:
        raise ValidationError('Metric should be in range 1, 32768')
