from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from datamap.validators import cell_ref_validator
from register.models import Tier

import uuid


class Datamap(models.Model):
    """A datamap in the system."""

    name = models.CharField(max_length=25)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=50, blank=True, default=uuid.uuid1)

    class Meta:
        unique_together = ("name", "tier")

    def get_absolute_url(self):
        return reverse('datamaps:datamap_detail', args=[str(self.slug)])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify("-".join([self.name, self.tier.name]))
        super().save(*args, **kwargs)


class DatamapLine(models.Model):

    DATAMAPLINE_TYPES = (
        ('Text', "TEXT"),
        ('Integer', "INTEGER"),
        ('Float', "FLOAT"),
        ('Date', "DATE"),
        ('Phone', "PHONE"),
    )

    """A single line in the datamap."""
    datamap = models.ForeignKey("Datamap", on_delete=models.CASCADE, related_name="datamaplines")
    key = models.CharField(max_length=100)
    data_type = models.CharField(max_length=10, choices=DATAMAPLINE_TYPES, default='Text')
    required = models.BooleanField(default=True)
    max_length = models.IntegerField(blank=True, null=True)
    sheet = models.CharField(max_length=50)
    cell_ref = models.CharField(max_length=10, validators=[cell_ref_validator], verbose_name="Cell Reference")

    class Meta:
        unique_together = ("datamap", "sheet", "cell_ref")

    def get_absolute_url(self):
        return reverse('datamaps:datamap_list')

    def __str__(self):
        return f"{self.key} for {self.datamap}"
