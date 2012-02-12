#from apps.registration.signals import user_registered
#from django.contrib.auth.models import User
#from core.profiles.models import Profile
#from apps.sprouts.models import Sprout
#from django.db import transaction
#
#@transaction.commit_on_success()
#def createProfile(sender, user, request, **kwargs):
#    """Create a UserProfile object each time a User is created ; and link it.
#        """
#    profile, created    = Profile.objects.get_or_create(user=user, sprout=sprout)
#    
#user_registered.connect(createProfile)
#