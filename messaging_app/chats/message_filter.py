from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class MessageFilter(DjangoFilterBackend):
    filter_backends = [DjangoFilterBackend,
                       SearchFilter,
                       OrderingFilter,]
   