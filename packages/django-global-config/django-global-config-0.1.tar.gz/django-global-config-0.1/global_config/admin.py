from django.contrib import admin
from django.forms import ModelForm

from .models import ConfigItem


class ConfigItemChangeForm(ModelForm):
    class Meta:
        model = ConfigItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'key':
                field.label = 'Value'


@admin.register(ConfigItem)
class ConfigItemAdmin(admin.ModelAdmin):
    form = ConfigItemChangeForm
    fields = ('key',)
    list_display = ('key', 'value', 'updated_at')

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj:
            fields += (obj.value_field_name,)
        return fields

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['key']
        return []
