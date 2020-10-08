import time

from django.db import models


class TimeStampMixin(models.Model):
    """
    Timestamp management for models
    """
    created_at = models.IntegerField(editable=False, default=int(time.time()))
    modify_at = models.IntegerField(default=int(time.time()))
    deleted_at = models.IntegerField(null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Update timestamps.
        """
        self.modify_at = int(time.time())
        return super().save(*args, **kwargs)

    def delete_now(self):
        self.deleted_at = int(time.time())


class NestedOrFlatSerializerMixin:
    """
    Modifys serializer's depth according to query parameter
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        nested = self.context.get("query")
        if nested is not None:
            if nested == 'nested':
                self.Meta.depth = 1
            else:
                self.Meta.depth = 0

    class Meta:
        abstract = True
