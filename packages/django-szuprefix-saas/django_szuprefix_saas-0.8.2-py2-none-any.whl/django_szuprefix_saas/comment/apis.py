# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django_szuprefix.api.mixins import UserApiMixin
from django_szuprefix_saas.saas.mixins import PartyMixin
from django_szuprefix_saas.saas.permissions import IsSaasWorker

from . import serializers, models, helper
from rest_framework import viewsets
from django_szuprefix.api.helper import register

__author__ = 'denishuang'


class CommentViewSet(PartyMixin, UserApiMixin, viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()
    permission_classes = [IsSaasWorker]
    filter_fields = {
        'content_type': ['exact'],
        'object_id': ['exact'],
        'user': ['exact'],
        'reply_count': ['gte', 'lte']
    }

    def filter_queryset(self, queryset):
        qset = super(CommentViewSet, self).filter_queryset(queryset)
        ct = self.request.query_params.get('content_type')
        if not ct:
            ctid = helper.get_comment_content_type_id()
            return qset.exclude(content_type=ctid)
        return qset


register(__package__, 'comment', CommentViewSet)


class RatingViewSet(PartyMixin, UserApiMixin, viewsets.ModelViewSet):
    serializer_class = serializers.RatingSerializer
    queryset = models.Rating.objects.all()
    permission_classes = [IsSaasWorker]
    filter_fields = {
        'content_type__app_label': ['exact'],
        'content_type__model': ['exact'],
        'content_type': ['exact'],
        'object_id': ['exact'],
        'user': ['exact']
    }

    def submit(self):
        pass


register(__package__, 'rating', RatingViewSet)
