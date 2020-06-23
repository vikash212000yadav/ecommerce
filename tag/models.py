from django.db import models


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
