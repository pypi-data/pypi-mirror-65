from pytz import utc
import datetime
from django.db import transaction
from push_notification.event_dispatcher.models import EventDispatcher


def emit_event_dispatcher(account_id, object_id, event_type, effective_at, is_uniq=False, meta_data=None):
    if is_uniq:
        return EventDispatcher.objects.get_or_create(
            object_id=object_id,
            account_id=account_id,
            meta_data=meta_data,
            event_type=event_type,
            defaults={
                'effective_at': effective_at,
            }
        )

    return EventDispatcher.objects.create(
        object_id=object_id,
        account_id=account_id,
        meta_data=meta_data,
        event_type=event_type,
        effective_at=effective_at,
    )


def discard_event_dispatcher(object_id, account_id, event_types):
    with transaction.atomic():
        event_dispatchers = EventDispatcher.objects.filter(
            object_id=object_id,
            event_type__in=event_types,
            account_id=account_id,
        ).order_by('created_at')

        for event_dispatcher in event_dispatchers:
            event_dispatcher.deleted_at = datetime.datetime.utcnow().replace(tzinfo=utc)
            event_dispatcher.save()
