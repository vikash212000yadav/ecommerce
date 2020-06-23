from django.urls import path

from tag.views import TagListView

urlpatterns = [
    path('tags/$', TagListView.as_view(), name='tag-list'),
]