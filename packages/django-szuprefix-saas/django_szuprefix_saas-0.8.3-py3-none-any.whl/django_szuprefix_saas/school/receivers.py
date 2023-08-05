# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_save
from django_szuprefix.auth.signals import to_get_user_profile
from django_szuprefix_saas.verify.models import Verify

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


@receiver(post_save, sender=Verify)
def create_student_after_verify(sender, **kwargs):
    created = kwargs.get('created')
    if created:
        return
    verify = kwargs.get('instance')
    if verify.category != helper.APPLY_VERIFY_CATEGORY:
        return
    if verify.target_type != ContentType.objects.get_for_model(models.Student):
        return
    d = verify.content
    from django.contrib.auth.models import User
    user = User.objects.get(id=d.get('user'))
    from django_szuprefix_saas.verify import choices
    if verify.status == choices.STATUS_PASS:
        helper.create_student_for_wechat_user(user.as_wechat_user)
    elif verify.status == choices.STATUS_REJECT:
        pass


def create_student_for_wechat_user(sender, **kwargs):
    wuser = kwargs['instance']
    helper.create_student_for_wechat_user(wuser)


def bind_create_student_for_wechat_user_receiver():
    b = access(settings, 'SCHOOL.STUDENT.AUTO_GEN_FROM_WECHAT_USER')
    if not b or b.lower() == 'false':
        return
    from django_szuprefix.wechat.models import User
    from django.db.models.signals import post_save
    post_save.connect(create_student_for_wechat_user, sender=User)


bind_create_student_for_wechat_user_receiver()
