from django.db import models


class Household(models.Model):
    name = models.CharField(max_length=100)
    data = models.JSONField(default=dict, blank=True)


class Individual(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    data = models.JSONField(default=dict, blank=True)
