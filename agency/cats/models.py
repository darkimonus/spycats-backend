from django.db import models
from django.core.validators import MaxValueValidator

from cats.validators import validate_breed


class SpyCat(models.Model):
    name = models.CharField(max_length=50)
    experience = models.PositiveSmallIntegerField(validators=[MaxValueValidator(15)])
    breed = models.CharField(max_length=50, validators=[validate_breed])
    salary = models.FloatField()
