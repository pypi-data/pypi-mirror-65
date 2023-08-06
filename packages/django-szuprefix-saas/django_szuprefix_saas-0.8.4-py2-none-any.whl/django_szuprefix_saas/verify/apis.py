# -*- coding:utf-8 -*-
from __future__ import division
from django_szuprefix.api.mixins import UserApiMixin
from django_szuprefix.utils.statutils import do_rest_stat_action
from django_szuprefix_saas.saas.mixins import PartyMixin
from rest_framework.viewsets import ModelViewSet

from . import models, serializers, stats
from rest_framework import mixins, decorators
from django_szuprefix.api.decorators import register


@register()
class VerifyViewSet(PartyMixin, UserApiMixin, ModelViewSet):
    queryset = models.Verify.objects.all()
    serializer_class = serializers.VerifySerializer
    filter_fields = {
        'category': ['exact'],
        'status': ['exact']
    }
    search_fields = ['name']

    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_verify)

    def perform_update(self, serializer):
        serializer.save(**self.get_serializer_save_args())
