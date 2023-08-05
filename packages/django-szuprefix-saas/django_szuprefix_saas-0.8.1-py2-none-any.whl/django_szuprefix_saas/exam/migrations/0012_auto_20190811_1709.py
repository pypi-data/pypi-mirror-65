# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-08-11 17:09
from __future__ import unicode_literals

from django.db import migrations, models


def add_owner(apps, schema_editor):
    Chapter = apps.get_model('course', 'Chapter')
    Course = apps.get_model('course', 'Course')
    Paper = apps.get_model('exam', 'Paper')
    from django.contrib.contenttypes.models import ContentType
    for cl in [Course, Chapter]:
        tid = ContentType.objects.get_for_model(cl).id
        for o in cl.objects.all():
            for p in o.exam_papers.all():
                Paper.objects.filter(id=p.id).update(owner_type=tid, owner_id=o.id)
                print tid, o.id, p.id, p.title


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('exam', '0011_auto_20190429_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='owner_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paper',
            name='owner_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.RunPython(add_owner),
    ]
