from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from tag.models import Tag
from tag.serializers import TagSerializer


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer