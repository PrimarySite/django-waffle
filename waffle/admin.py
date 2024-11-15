from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin.widgets import ManyToManyRawIdWidget
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from waffle.models import Sample, Switch


class BaseAdmin(admin.ModelAdmin):
    search_fields = ('name', 'note')

    def get_actions(self, request):
        actions = super(BaseAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


def enable_for_all(ma, request, qs):
    # Iterate over all objects to cause cache invalidation.
    for f in qs.all():
        f.everyone = True
        f.save()


def disable_for_all(ma, request, qs):
    # Iterate over all objects to cause cache invalidation.
    for f in qs.all():
        f.everyone = False
        f.save()


def delete_individually(ma, request, qs):
    # Iterate over all objects to cause cache invalidation.
    for f in qs.all():
        f.delete()


enable_for_all.short_description = _('Enable selected flags for everyone')
disable_for_all.short_description = _('Disable selected flags for everyone')
delete_individually.short_description = _('Delete selected')


class InformativeManyToManyRawIdWidget(ManyToManyRawIdWidget):
    """Widget for ManyToManyField to Users.

    Will display the names of the users in a parenthesised list after the
    input field. This widget works with all models that have a "name" field.
    """
    def label_and_url_for_value(self, values):
        names = []
        key = self.rel.get_related_field().name
        for value in values:
            try:
                name = self.rel.model._default_manager \
                    .using(self.db) \
                    .get(**{key: value})
                names.append(escape(str(name)))
            except self.rel.model.DoesNotExist:
                names.append('<missing>')
        return "(" + ", ".join(names) + ")", ""


class FlagAdmin(BaseAdmin):
    actions = [enable_for_all, disable_for_all, delete_individually]
    list_display = ('name', 'note', 'everyone', 'percent', 'superusers',
                    'staff', 'authenticated', 'languages')
    list_filter = ('everyone', 'superusers', 'staff', 'authenticated')
    raw_id_fields = ('users', )
    ordering = ('-id',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'users':
            kwargs.pop('request', None)
            kwargs['widget'] = \
                InformativeManyToManyRawIdWidget(db_field.remote_field,
                                                 self.admin_site,
                                                 using=kwargs.get("using"))
            return db_field.formfield(**kwargs)
        return super(FlagAdmin, self).formfield_for_dbfield(db_field, **kwargs)


def enable_switches(ma, request, qs):
    for switch in qs:
        switch.active = True
        switch.save()


def disable_switches(ma, request, qs):
    for switch in qs:
        switch.active = False
        switch.save()


enable_switches.short_description = _('Enable selected switches')
disable_switches.short_description = _('Disable selected switches')


class SwitchAdmin(BaseAdmin):
    actions = [enable_switches, disable_switches, delete_individually]
    list_display = ('name', 'active', 'note', 'created', 'modified')
    list_filter = ('active',)
    ordering = ('-id',)


class SampleAdmin(BaseAdmin):
    actions = [delete_individually]
    list_display = ('name', 'percent', 'note', 'created', 'modified')
    ordering = ('-id',)


admin.site.register(Sample, SampleAdmin)
admin.site.register(Switch, SwitchAdmin)
