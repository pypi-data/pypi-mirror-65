"""Declares :class:`ReadonlyModelAdminMixin`."""


class ReadonlyModelAdminMixin:

    def get_actions(self, request):
        actions = super().get_actions(request)
        del_action = "delete_selected"
        if del_action in actions:
            del actions[del_action]
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass

    def delete_model(self, request, obj):
        pass

    def save_related(self, request, form, formsets, change):
        pass

    def get_readonly_fields(self, request, obj=None):
        return list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
