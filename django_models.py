from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        out = dict()

        for field in self._meta.fields:
            out[field.name] = getattr(self, field.name)

            return out

    class Meta:
        abstract = True
