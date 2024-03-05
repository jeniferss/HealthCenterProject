from django.db import models


class DateTimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        abstract = True


class StripMixin:
    def clean(self):
        for field in self._meta.fields:
            if not isinstance(field, models.CharField):
                continue

            value = getattr(self, field.name, None)
            if not value:
                continue

            setattr(self, field.name, value.strip())


class BaseModel(DateTimeMixin, StripMixin):
    class Meta:
        abstract = True
