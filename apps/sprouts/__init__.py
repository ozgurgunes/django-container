from django.db import transaction
#from apps.registration.signals import user_activated
from django.contrib.auth.models import User
from apps.sprouts.models import Sprout

@transaction.commit_on_success()
def createPlant(sender, user, request, **kwargs):
    """Create a UserProfile object each time a User is created ; and link it.
        """
    sprout, created = Sprout.objects.get_or_create(user=user, title=user.username)
    
#user_activated.connect(createPlant)