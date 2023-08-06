from django.db import models
from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.core import serializers


def get_content_type_for_model(obj):
    # Since this module gets imported in the application's root package,
    # it cannot import models from other applications at the module level.
    from django.contrib.contenttypes.models import ContentType
    return ContentType.objects.get_for_model(obj, for_concrete_model=False)

'''
changed_field = [
    {
        "added": {
            "name": "\u0422\u0438\u043f \u0441\u043f\u043e\u0440\u0442\u0430 \u0444\u0438\u0442\u043d\u0435\u0441-\u0446\u0435\u043d\u0442\u0440\u0430", 
            "object": "FitnessSportType object (518)",
            },
        "changed": {
            "fields": ["phone", "full_name"] 
        }
    }
]
'''


def changed_message(changed_field, old, new):
    message = ''
    for i in changed_field:
        if "changed" in i:
            if "fields" in i["changed"]:
                for field in i["changed"]["fields"]:
                    try:
                        message += f"field: {field}"
                        old_field = eval('old["fields"]["' + field + '"]')
                        new_field = eval('new.' + field)
                        message += f", old: {str(old_field)[:50]}, new: {str(new_field)[:50]}\n"
                    except:
                        pass
        if "added" in i:
            for key, value in i["added"].items():
                try:
                    message += f"added: {key} - {value}\n"
                except:
                    pass
    return message


class CustomModelAdmin(admin.ModelAdmin):

    old_instance = {}

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        try:
            old_obj = obj._meta.model.objects.get(id=obj.id)
            old_obj_str = serializers.serialize('json', [old_obj, ])
            old_obj_str = old_obj_str.replace("null", "None").replace("false", "False").replace("true", "True")
            old_obj_json = eval(old_obj_str)[0]
            self.old_instance = old_obj_json
        except Exception as e:
            pass
        obj.save()

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        try:
            old_obj_str = serializers.serialize('json', [obj, ])
            old_obj_str = old_obj_str.replace("null", "None").replace("false", "False").replace("true", "True")
            old_obj_json = eval(old_obj_str)[0]
            self.old_instance = old_obj_json
        except:
            pass
        obj.delete()

    def log_addition(self, request, object, message):
        """
        Log that an object has been successfully added.

        The default implementation creates an admin LogEntry object.
        """
        from django.contrib.admin.models import LogEntry, ADDITION
        message = changed_message(message, self.old_instance, object)
        return LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=get_content_type_for_model(object).pk,
            object_id=object.pk,
            object_repr=str(object),
            action_flag=ADDITION,
            change_message=message,
        )

    def log_change(self, request, object, message):
        """
        Log that an object has been successfully changed.

        The default implementation creates an admin LogEntry object.
        """
        from django.contrib.admin.models import LogEntry, CHANGE
        message = changed_message(message, self.old_instance, object)
        return LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=get_content_type_for_model(object).pk,
            object_id=object.pk,
            object_repr=str(object),
            action_flag=CHANGE,
            change_message=message,
        )

    def log_deletion(self, request, object, object_repr):
        """
        Log that an object will be deleted. Note that this method must be
        called before the deletion.

        The default implementation creates an admin LogEntry object.
        """
        from django.contrib.admin.models import LogEntry, DELETION
        message = str(self.old_instance)
        return LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=get_content_type_for_model(object).pk,
            object_id=object.pk,
            object_repr=object_repr,
            action_flag=DELETION,
            change_message=message
        )


