import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from push_notification.event.interfaces import emit_event


class EventDispatcherManager(models.Manager):
    def actual(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class EventDispatcher(models.Model):
    event_dispatcher_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    event_type = models.CharField(max_length=254)
    account_id = models.UUIDField(null=True, blank=True)
    object_id = models.UUIDField(null=True, blank=True)
    meta_data = JSONField(null=True, blank=True)
    retry_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    effective_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)

    objects = EventDispatcherManager()

    class Meta:
        verbose_name = "event_dispatcher"
        verbose_name_plural = "event_dispatchers"

    def emit_event(self, event_type, account_id=None, object_id=None, **kwargs):
        account_id = account_id or self.account_id
        event_type = event_type or self.event_type
        object_id = object_id or self.object_id

        return emit_event(
            event_type=event_type.value,
            object_id=object_id,
            object_type=self._meta.db_table,
            account_id=account_id,
            **kwargs,
        )

    def save(self, *args, **kwargs):
        self.retry_count += 1
        return super().save(*args, **kwargs)
