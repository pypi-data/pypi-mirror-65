# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from . import models
COMMENT_CONTENT_TYPE_ID = None

def get_comment_content_type_id () :
    global COMMENT_CONTENT_TYPE_ID
    if COMMENT_CONTENT_TYPE_ID is None:
        COMMENT_CONTENT_TYPE_ID = ContentType.objects.get_for_model(models.Comment).id
    return COMMENT_CONTENT_TYPE_ID