from django.contrib import admin

# Register your models here.
# vim: set fileencoding=utf-8 :
from django.contrib import admin

from . import models


class ComponentAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('name',)


class CompositionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('name',)


class SMRInlineAdmin(admin.TabularInline):
    model = models.SMR


class ASMRInlineAdmin(admin.TabularInline):
    model = models.ASMR


class SpecialtyAdmin(admin.ModelAdmin):
    inlines = [SMRInlineAdmin, ASMRInlineAdmin]
    list_display = (
        'id',
        'name',
        'bdpm_id',
        'cis_code',
        'authorization_holder',
        'composition_quantity',
        'composition_type',
    )
    list_filter = (
        'composition_type',
        'id',
        'name',
        'bdpm_id',
        'cis_code',
        'authorization_holder',
        'composition_quantity',
        'composition_type',
    )
    raw_id_fields = ('composition_components',)
    search_fields = ('name',)


class ComponentRelationAdmin(admin.ModelAdmin):

    list_display = ('id', 'component', 'specialty', 'dosage')
    list_filter = (
        'component',
        'specialty',
        'id',
        'component',
        'specialty',
        'dosage',
    )


class PresentationsAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'cip_7',
        'cip_13',
        'marketing_start_date',
        'marketing_stop_date',
        'price',
        'refund_rate',
    )
    list_filter = (
        'marketing_start_date',
        'marketing_stop_date',
        'id',
        'name',
        'cip_7',
        'cip_13',
        'marketing_start_date',
        'marketing_stop_date',
        'price',
        'refund_rate',
    )
    search_fields = ('name',)


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Component, ComponentAdmin)
_register(models.CompositionType, CompositionTypeAdmin)
_register(models.Specialty, SpecialtyAdmin)
_register(models.ComponentRelation, ComponentRelationAdmin)
_register(models.Presentations, PresentationsAdmin)
