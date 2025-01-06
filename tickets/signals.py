from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:  # Only for new users
        # Assign the user to the "User" group by default
        user_group, created = Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)
        print(f"User {instance.username} added to the User group.")