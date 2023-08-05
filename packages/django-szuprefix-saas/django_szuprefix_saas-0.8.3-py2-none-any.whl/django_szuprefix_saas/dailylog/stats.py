# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from . import models
from django.db.models import Count, Sum, Max
from django_szuprefix.utils import statutils


def stats_stat(qset=None, measures=None, period=None):
    qset = qset if qset is not None else models.Stat.objects.all()
    qset = statutils.using_stats_db(qset)
    dstat = statutils.DateStat(qset, 'the_date')
    funcs = {
        'daily': lambda: dstat.stat(period, count_field='id', distinct=True),
    }
    return dict([(m, funcs[m]()) for m in measures])


def stats_record(qset=None, measures=None, period=None):
    qset = qset if qset is not None else models.Record.objects.all()
    qset = statutils.using_stats_db(qset)
    dstat = statutils.DateStat(qset, 'the_date')
    funcs = {
        'daily': lambda: dstat.group_by(period, measures=[Count('user', distinct=True), Sum('value')]),
        # 'exercise_done': lambda : dstat.group_by(measures=[Sum('value'), Count('user', distinct=True)]),
        'clazz': lambda: statutils.group_by(
            dstat.get_period_query_set(period),
            'user__as_school_student__clazz__name',
            measures=[Count('user', distinct=True), Sum('value')], sort="-"),
        'course': lambda: statutils.count_by_generic_relation(
            dstat.get_period_query_set(period),
            "course_course__name",
            count_field='user_id',
            distinct=True, sort="-"),
        'video': lambda: statutils.group_by_with_generic_relation(
            dstat.get_period_query_set(period).filter(owner_type_id=57),
            'owner',
            measures=[Sum('value'), Count('user_id', distinct=True)],
            trans_map={'media.video': ['lecturer__name', 'name']}
        ),
        'student_course': lambda: statutils.group_by_with_generic_relation(
            dstat.get_period_query_set(period),
            "user__as_school_student__clazz__name,user__as_school_student__name,owner",
            measures=[Max('value')],
            trans_map={'exam.paper': ['title']}
        ),
    }
    return dict([(m, funcs[m]()) for m in measures])
