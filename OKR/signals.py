from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import OKR, Objective, Formula, Source, Log

from math import ceil

@receiver(post_save, sender=OKR)
def create_log(sender, instance=None, created=False, **kwargs):
    if created:
        log = Log.objects.create(
            okr=instance,
            note=instance.note,
            created_by=instance.created_by,
            updated_by=instance.updated_by,
            created_at=instance.created_at,
            updated_at=instance.updated_at
        )
        log.save()

@receiver(pre_save, sender=OKR)
def calculate_ratio(sender, instance: OKR, created=False, **kwargs):
    if instance.result != '' and instance.result != None:
        instance.ratio = (instance.result / instance.norm) * instance.weight
    print(instance.ratio)

@receiver(pre_save, sender=OKR)
def get_quarter(sender, instance: OKR, created=False, **kwargs):
    month = instance.deadline.month
    year = instance.deadline.year
    quarter = ceil(month / 4)

    instance.deadline_quarter = f'Q{quarter}'
    instance.deadline_year = year
    instance.deadline_month = month


