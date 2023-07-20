from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Employee

@receiver(pre_save, sender=Employee)
def update_manage(sender, instance=None, created=False, **kwargs):
    sub_employee = instance.manages
    if sub_employee.exists():
        instance.is_manager = True
    else:
        instance.is_manager = False
        