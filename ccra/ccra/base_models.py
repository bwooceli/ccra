import uuid

from django.db import models


# base class that has a guid field as the primary key and sets the auto_admin_reg to True
class BaseCcraModel(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    auto_admin_reg = True

    def save(self, *args, **kwargs):
        # for each model property, if the name is "name" or "title", strip the value
        for field in self._meta.get_fields():
            if field.name == "name" or field.name == "title":
                setattr(self, field.name, getattr(self, field.name).strip())

        super().save(*args, **kwargs)

    class Meta:
        abstract = True
