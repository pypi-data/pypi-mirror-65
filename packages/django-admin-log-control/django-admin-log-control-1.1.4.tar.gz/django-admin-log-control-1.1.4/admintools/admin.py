from django.contrib import admin
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.urls import reverse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'
    list_filter = ('action_flag', )

    search_fields = [
        'object_repr',
        'change_message',
        'user__full_name',
        'user__phone',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag_',
        'change_message_',
    ]

    def get_readonly_fields(self, request, obj=None):
        return self.model._meta.get_all_field_names()

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def action_flag_(self, obj):
        flags = {
            1: "Addition",
            2: "Changed",
            3: "Deleted",
        }
        return flags[obj.action_flag]

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr.replace('{', '(').replace('}', ')')),
            )
        return format_html(link)

    def change_message_(self, obj):
        html = '<ol type="1">'
        for line in obj.change_message.split('\n')[:-1]:
            line = line.replace('{', "(").replace("}", ')')
            line = line.replace("old", '<span style="color:red">old</span>')
            line = line.replace("new", '<span style="color:green">new</span>')
            html += f'<li> {line} </li>'
        html += '</ol>'
        return format_html(html)

    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'
