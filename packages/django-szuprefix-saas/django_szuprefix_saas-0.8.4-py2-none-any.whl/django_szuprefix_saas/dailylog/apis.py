# -*- coding:utf-8 -*-
from __future__ import division, unicode_literals
from django_szuprefix.api.mixins import UserApiMixin
from django_szuprefix.utils.statutils import do_rest_stat_action
from django_szuprefix_saas.saas.mixins import PartyMixin
from rest_framework.response import Response

__author__ = 'denishuang'
from . import models, serializers,stats
from rest_framework import viewsets, decorators, mixins
from django_szuprefix.api.decorators import register


@register()
class DailyLogViewSet(PartyMixin, UserApiMixin, viewsets.ModelViewSet):
    queryset = models.DailyLog.objects.all()
    serializer_class = serializers.DailyLogSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'the_date': ['exact', 'gte', 'lte'],
    }

    @decorators.list_route(['POST'])
    def write(self, request):
        user = request.user
        for k, v in request.data.iteritems():
            log, created = self.party.dailylog_dailylogs.get_or_create(user=user, the_date=k)
            log.context.update(v)
            log.save()
        return Response({'detail': 'success'})


@register()
class StatViewSet(PartyMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Stat.objects.all()
    serializer_class = serializers.StatSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'the_date': ['exact', 'gte', 'lte'],
        'metics': ['exact'],
        'owner_id': ['exact', 'isnull']
    }

    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_stat)

@register()
class RecordViewSet(PartyMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Record.objects.all()
    serializer_class = serializers.RecordSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'the_date': ['exact', 'gte', 'lte'],
        'metics': ['exact'],
        'owner_id': ['exact', 'isnull'],
        'owner_type': ['exact',],
        'user': ['exact',]
    }

    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_record)
