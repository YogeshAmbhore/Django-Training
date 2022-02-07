from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import PMProfile, DevProfile
from django.db.models.signals import post_save, post_delete


def createManager(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = PMProfile.objects.create(
            user = user,
        )

def deleteManager(sender, instance, **kwargs):
    user = instance.user
    user.delete()


# def createDeveloper(sender, instance, created, **kwargs):
#     if created:
#         user = instance
#         if user.is_developer:
#             group = Group.objects.get(name='developer')
#             user.groups.add(group)

post_save.connect(createManager, sender = User)

post_delete.connect(deleteManager, sender = PMProfile)

# post_save.connect(createDeveloper, sender=User)

# def managercreated(sender, instance, created, **kwargs):
#     print('profile saved')
#     print('instance: ', instance)
#     print('CREATED: ', created)

# post_save.connect(managercreated, sender=PMProfile)