# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.dispatch import receiver
from django.db.models.signals import post_save
from django_szuprefix.auth.signals import to_get_user_profile

from . import models, helper, serializers
from django.conf import settings
from django_szuprefix.utils.datautils import access
import logging

log = logging.getLogger("django")


@receiver(post_save, sender=models.School)
def init_grade(sender, **kwargs):
    try:
        school = kwargs['instance']
        if school.grades.count() == 0:
            helper.gen_default_grades(school)
    except Exception, e:
        log.error("init_grade error: %s" % e)


@receiver(post_save, sender=models.Grade)
def init_session(sender, **kwargs):
    try:
        grade = kwargs['instance']
        school = grade.school
        helper.gen_default_session(school, grade.number - 1)
    except Exception, e:
        log.error("init_session error: %s" % e)


@receiver(post_save, sender=models.Student)
def add_student_to_clazz_names(sender, **kwargs):
    try:
        student = kwargs['instance']
        clazz = student.clazz
        ns = clazz.student_names
        # print student.name, ns
        if student.name not in ns:
            clazz.student_names.append(student.name)
            clazz.save()
    except Exception, e:
        import traceback
        log.error("add_student_to_clazz_names error: %s, %s", e, traceback.format_exc())


# @receiver(post_save, sender=Worker)
# def init_student(sender, **kwargs):
#     # try:
#     worker = kwargs['instance']
#     # print worker
#     if worker.position != '学生':
#         return
#     tasks.init_student.delay(worker.id)
#     # except Exception, e:
#     #     log.error("init_student error: %s" % e)

@receiver(to_get_user_profile)
def get_school_profile(sender, **kwargs):
    user = kwargs['user']
    if hasattr(user, 'as_school_student'):
        return serializers.CurrentStudentSerializer(user.as_school_student, context=dict(request=kwargs['request']))
    if hasattr(user, 'as_school_teacher'):
        return serializers.CurrentTeacherSerializer(user.as_school_teacher, context=dict(request=kwargs['request']))


def create_student_for_wechat_user(sender, **kwargs):
    wuser = kwargs['instance']
    user = wuser.user
    if hasattr(user, 'as_school_student'):
        return
    s = access(settings, 'SCHOOL.STUDENT.AUTO_GEN_FOR_SCHOOL')
    school = models.School.objects.filter(id=s).first()
    grade = school.grades.first()
    from datetime import datetime
    year = datetime.now().year
    session, created = school.sessions.get_or_create(number=year)
    clazz, created = school.classes.get_or_create(
        name="2020级微信公众号体验班",
        defaults=dict(
            entrance_session=session,
            grade=grade)
    )
    if not hasattr(user, 'as_saas_worker'):
        worker, created = school.party.workers.get_or_create(
            number=wuser.openid,
            defaults=dict(
                name=wuser.nickname,
                user=user,
                position="学生"
            )
        )

    student, created = school.students.get_or_create(
        number=wuser.openid,
        defaults=dict(
            user=user,
            name=wuser.nickname,
            clazz=clazz,
            is_bind=True,
            is_formal=False,
            entrance_session=session,
            grade=grade
        ))

    clazz.students.add(student)


def bind_create_student_for_wechat_user_receiver():
    b = access(settings, 'SCHOOL.STUDENT.AUTO_GEN_FROM_WECHAT_USER')
    if not b or b.lower() == 'false':
        return
    from django_szuprefix.wechat.models import User
    from django.db.models.signals import post_save
    from .receivers import create_student_for_wechat_user
    post_save.connect(create_student_for_wechat_user, sender=User)


bind_create_student_for_wechat_user_receiver()
