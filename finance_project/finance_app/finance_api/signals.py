from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User

@receiver(post_save, sender=User)
def create_predefined_categories(sender,instance,created, **kwargs):
    """
    After a User is created, it is populated with 
    """
