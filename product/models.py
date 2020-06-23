from django.db import models

# Create your models here.
from tag.models import Tag
from user.models import Seller


class Product(models.Model):
    tag_set = models.ManyToManyField(Tag)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title