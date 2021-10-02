from rest_framework import viewsets
from rest_framework.renderers import BrowsableAPIRenderer

from account.render import MyJSONRenderer


class MyViewSet(viewsets.ModelViewSet):
    pagination_class = None
    renderer_classes = (MyJSONRenderer, BrowsableAPIRenderer)