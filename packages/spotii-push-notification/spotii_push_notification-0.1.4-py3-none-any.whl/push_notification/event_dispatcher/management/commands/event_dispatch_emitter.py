import datetime
import time
import traceback
from django.core.management.base import BaseCommand
from django.db import OperationalError
from django.db import transaction
from pytz import utc
from django.conf import settings
from push_notification.event_dispatcher.models import EventDispatcher


class Command(BaseCommand):
    help = "It creates events for effective at"

    process_batch = settings.PUSH_NOTIFICATIONS.get('PROCESS_BUTCH', 500)

    def get_event_dispatchers_qs(self):
        return EventDispatcher.objects.actual.filter(
            effective_at__lt=datetime.datetime.utcnow().replace(tzinfo=utc)
        ).select_for_update(skip_locked=True).order_by('effective_at')

    def handle(self, *args, **kwargs):
        self.stdout.write("event dispatch emitter started")

        while True:
            try:
                event_dispatchers = self.get_event_dispatchers_qs()[:self.process_batch]
                with transaction.atomic():
                    for event_dispatcher in event_dispatchers.all():
                        self.process(event_dispatcher)

            except Exception as e:
                traceback.print_exc()
            time.sleep(1)

    def process(self, event_dispatcher):
        event_dispatcher.emit_event()
