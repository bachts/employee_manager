from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OKR, Objective, Formula, Source, Log

@receiver(post_save, sender=OKR)
def create_log(sender, instance=None, created=False, **kwargs):
    if created:
        log, is_created = Log.objects.get_or_create(okr_id=instance.id,
                                                    note=instance.note,
                                                    created_by=instance.created_by,
                                                    updated_by=instance.updated_by,
                                                    created_at=instance.created_at,
                                                    updated_at=instance.updated_at)
        log.save()