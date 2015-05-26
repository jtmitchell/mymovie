# -*- coding: utf-8 -*-
import csv
import datetime

from django.http import HttpResponse
from django.utils.timezone import localtime, get_current_timezone


def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True, force_fields=None):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    if 'force_field' is True, you can give as a list of string whatever django admin can read in display_list
    else it will check if the fields are in the model and reduce the list

    # example usage:
    class SubscriberAdmin(admin.ModelAdmin):

        def display_city(self, obj):
            return obj.address.city #address being i.e. a OneToOne relation to Subscriber

        raw_id_fields = ('logged_in_as',)
        list_display = ('email', 'date', 'logged_in_as', 'display_city',)
        actions = [export_as_csv_action("Export selected emails as CSV file", fields=list_display, header=True, force_fields=True),]

    admin.site.register(UpdatesSubscriber, SubscriberAdmin)
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/2020/
        extended for being able to give list_display as fields and work with admin-defined functions
        """
        opts = modeladmin.model._meta
        if not force_fields:
            field_names = set([field.name for field in opts.fields])
            if fields:
                fieldset = set(fields)
                field_names = field_names & fieldset
        elif fields:
            field_names = set(fields)
        else:
            raise("option force_fields can only be used in parallel with option fields")
        if exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            row = []
            for field in field_names:
                value = None
                try:
                    value = getattr(obj, field)
                except AttributeError:
                    value = getattr(modeladmin, field)(obj)
                except:
                    raise
                if isinstance(value, datetime.datetime) or isinstance(value, datetime.date):
                    row.append(str(localtime(value, get_current_timezone())).encode('utf-8'))
                else:
                    row.append(str(value).encode('utf-8'))
            writer.writerow(row)
        return response
    export_as_csv.short_description = description
    return export_as_csv
