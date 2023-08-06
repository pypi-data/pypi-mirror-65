# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from . import choices


def sync_qcloud_vod_info(v):
    from xyz_qcloud import vod
    from xyz_qcloud.utils import access as A
    fid = v.context.get('fileId') or v.context.get('FileId')
    if not fid:
        return
    vc = v.context = A(vod.get_media_info(fid), 'MediaInfoSet.0')
    v.cover_url = A(vc, 'BasicInfo.CoverUrl')
    v.duration = A(vc, 'MetaData.Duration')
    v.size = A(vc, 'TranscodeInfo.TranscodeSet.0.Size')
    v.status = choices.STATUS_DONE
    v.save()
