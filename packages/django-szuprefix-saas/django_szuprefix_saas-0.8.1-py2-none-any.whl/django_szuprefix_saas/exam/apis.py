# -*- coding:utf-8 -*-
from __future__ import division
from django_szuprefix.utils.statutils import do_rest_stat_action
from django_szuprefix.api.mixins import UserApiMixin, BatchActionMixin
from django_szuprefix_saas.saas.mixins import PartyMixin
from .apps import Config

__author__ = 'denishuang'
from . import models, serializers, stats
from rest_framework import viewsets, decorators
from django_szuprefix.api.helper import register


class PaperViewSet(PartyMixin, UserApiMixin, BatchActionMixin, viewsets.ModelViewSet):
    queryset = models.Paper.objects.all()
    serializer_class = serializers.PaperFullSerializer
    search_fields = ('title',)
    filter_fields = {
        'id': ['in', 'exact'],
        'is_active': ['exact'],
        'is_break_through': ['exact'],
        'content': ['contains'],
        'tags': ['exact'],
        'owner_type': ['exact'],
        'owner_id': ['exact', 'in'],
    }
    ordering_fields = ('is_active', 'title', 'create_time', 'questions_count')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PaperSerializer
        return super(PaperViewSet, self).get_serializer_class()

    @decorators.list_route(['POST'])
    def batch_active(self, request):
        return self.do_batch_action('is_active', True)


    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_paper)

register(Config.label, 'paper', PaperViewSet)


class AnswerViewSet(PartyMixin, UserApiMixin, viewsets.ModelViewSet):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    filter_fields = ('paper', 'user')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AnswerListSerializer
        return super(AnswerViewSet, self).get_serializer_class()

    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_answer)


register(Config.label, 'answer', AnswerViewSet)


class StatViewSet(PartyMixin, UserApiMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Stat.objects.all()
    serializer_class = serializers.StatSerializer
    filter_fields = ('paper',)


register(Config.label, 'stat', StatViewSet)


class PerformanceViewSet(PartyMixin, UserApiMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Performance.objects.all()
    serializer_class = serializers.PerformanceSerializer
    filter_fields = {'paper': ['exact', 'in'], 'user': ['exact']}
    search_fields = ('paper__title', 'user__first_name')
    ordering_fields = ('score', 'update_time')


register(Config.label, 'performance', PerformanceViewSet)


class FaultViewSet(PartyMixin, UserApiMixin, viewsets.ModelViewSet):
    queryset = models.Fault.objects.all()
    serializer_class = serializers.FaultSerializer
    filter_fields = {
        'paper': ['exact', 'in'],
        'question_id': ['exact'],
        'corrected': ['exact'],
        'user': ['exact']
    }
    ordering_fields = ['times', 'update_time']

    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_fault)


register(Config.label, 'fault', FaultViewSet)


class ExamViewSet(PartyMixin, BatchActionMixin, viewsets.ModelViewSet):
    queryset = models.Exam.objects.all()
    serializer_class = serializers.ExamSerializer
    search_fields = ('name',)
    filter_fields = {
        'name': ['exact', 'in'],
        'is_active': ['exact', 'in'],
        'owner_type': ['exact'],
        'owner_id': ['exact', 'in'],
        'begin_time': ['gte', 'lte']
    }

    @decorators.list_route(['POST'])
    def batch_active(self, request):
        return self.do_batch_action('is_active', True)

register(Config.label, 'exam', ExamViewSet)
