from django.contrib import admin

# Register your models here.
# vim: set fileencoding=utf-8 :
from django.contrib import admin
import nested_admin

from . import models


class ComponentAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('name',)


class CompositionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('name',)


class SMRInlineAdmin(nested_admin.NestedTabularInline):
    model = models.SMR
    extra = 0

class ASMRInlineAdmin(nested_admin.NestedTabularInline):
    model = models.ASMR
    extra = 0


class PresentationsInlineAdmin(nested_admin.NestedStackedInline):
    model = models.Presentations
    extra = 0


# through : to use through model in admin via direct inline
class ComponentInlineAdmin(nested_admin.NestedTabularInline):
    model = models.Composition.components.through
    extra = 0


class CompositionAdmin(nested_admin.NestedModelAdmin):
    model = models.Composition
    inlines = [ComponentInlineAdmin]


class CompositionInlineAdmin(nested_admin.NestedStackedInline):
    model = models.Composition
    inlines = [ComponentInlineAdmin]
    extra = 0


class SpecialtyAdmin(nested_admin.NestedModelAdmin):
    inlines = [SMRInlineAdmin, ASMRInlineAdmin, PresentationsInlineAdmin, CompositionInlineAdmin]
    list_display = (
        'id',
        'name',
        'bdpm_id',
        'cis_code',
        'authorization_holder',
    )
    list_filter = (
        'id',
        'name',
        'bdpm_id',
        'cis_code',
        'authorization_holder',
    )
    search_fields = ('name',)


class ComponentRelationAdmin(admin.ModelAdmin):

    list_display = ('id', 'component', 'dosage')
    list_filter = (
        'component',
        'id',
        'dosage',
    )





def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Component, ComponentAdmin)
_register(models.CompositionType, CompositionTypeAdmin)
_register(models.Specialty, SpecialtyAdmin)
_register(models.ComponentRelation, ComponentRelationAdmin)
_register(models.Composition, CompositionAdmin)
#_register(models.Presentations, PresentationsAdmin)
