from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import DestroyAPIView
""" Import from Local App. """
from taggit.models import Tag
from djangotags.rest_api.serializers import TagSerializer


class TagListViewSet(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagRetrieveViewSet(RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "tag_slug"


class TagUpdateViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "tag_slug"


class TagDestroyViewSet(DestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "tag_slug"
