"""Forms for model editing."""

from typing import Any

from django import forms
from django.urls import reverse

from .models import Config, DataType


class ConfigAdminForm(forms.ModelForm):
    """Form used for editing Config objects in the django admin."""

    def __init__(self, *args: Any, **kwargs: Any):
        """Constructor.

        Replaces the default widgets with new ones."""

        super().__init__(*args, **kwargs)

        self.fields["data_type"].widget = forms.Select(
            choices=self.fields["data_type"].widget.choices,
            attrs={
                "class": "aboutconfig-type-field",
                "data-url": reverse("admin:ac-fetch-value-field"),
                "data-instance-pk": self.instance.pk or "",
            },
        )

        data_type = self.get_data_type()

        original_field = self.fields["value"]
        field_class = original_field.__class__
        self.fields["value"] = field_class(
            initial=original_field.initial,
            widget=data_type.get_widget_class()(**data_type.widget_args),
        )

    class Meta:
        model = Config
        fields = ("data_type", "key", "value", "allow_template_use")
        readonly_fields = ("default_value",)

    def get_data_type(self) -> DataType:
        """Get data type to use when figuring out how to render the value field."""

        try:
            return DataType.objects.get(pk=self.data["data_type"])
        except (KeyError, DataType.DoesNotExist):
            pass

        try:
            return self.instance.data_type
        except DataType.DoesNotExist:
            return DataType.objects.get(name="String")
