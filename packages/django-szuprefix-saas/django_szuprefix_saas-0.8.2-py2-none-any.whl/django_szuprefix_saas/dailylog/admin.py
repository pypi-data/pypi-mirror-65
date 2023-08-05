from django.contrib import admin

from . import models


@admin.register(models.DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'user', 'the_date')
    raw_id_fields = ('party', 'user')
    readonly_fields = ('party',)

@admin.register(models.Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('the_date', 'owner_type', 'owner_id', 'metics', 'value', 'user_count')
    raw_id_fields = ('party', )
    readonly_fields = ('party',)
    date_hierarchy = 'the_date'
    list_filter = ('owner_type', 'metics')

@admin.register(models.Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('the_date', 'owner_type', 'owner_id', 'metics', 'value', 'user')
    raw_id_fields = ('party', 'owner_type', 'user')
    readonly_fields = ('party', 'user')
    date_hierarchy = 'the_date'
    list_filter = ('owner_type', 'metics')
