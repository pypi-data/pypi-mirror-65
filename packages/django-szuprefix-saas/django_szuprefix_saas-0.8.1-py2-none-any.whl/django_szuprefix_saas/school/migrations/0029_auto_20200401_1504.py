# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-04-01 15:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0028_teacher_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ('party', 'name'), 'permissions': (('view_all_teacher', '\u67e5\u770b\u6240\u6709\u8001\u5e08'),), 'verbose_name': '\u8001\u5e08', 'verbose_name_plural': '\u8001\u5e08'},
        ),
        migrations.AddField(
            model_name='student',
            name='is_formal',
            field=models.BooleanField(default=True, verbose_name='\u6b63\u5f0f'),
        ),
        migrations.AlterField(
            model_name='clazzcourse',
            name='clazz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='clazz_course_relations', to='school.Clazz', verbose_name='\u73ed\u7ea7'),
        ),
        migrations.AlterField(
            model_name='clazzcourse',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='clazz_course_relations', to='course.Course', verbose_name='\u8bfe\u7a0b'),
        ),
    ]
