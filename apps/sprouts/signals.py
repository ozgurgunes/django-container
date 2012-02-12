import datetime, logging
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete
from apps.sprouts.models import Leaf

logger = logging.getLogger("apps.sprouts.signals")

def add_leaf_signal(sender, instance, user=None, sprout=None, date_created=None, **kwargs):
	"""
	This is a generic singal for adding an object to the Sprout.

	"""
	ctype = ContentType.objects.get_for_model(instance)
	obj, created = Leaf.objects.get_or_create(
		content_type=ctype,
		object_id=instance.id,
        defaults={
            'user': instance.user,
            'sprout': instance.sprout,
            'date_created': datetime.datetime.now()
            })

def delete_leaf_signal(sender, instance, **kwargs):
	"""
	This is a generic singal to delete related Leaf when an object is deleted.

	"""
	ctype = ContentType.objects.get_for_model(instance)
	try:
		leaf = Leaf.objects.get(content_type=ctype, object_id=instance.id)
		leaf.delete()
	except Leaf.MultipleObjectsReturned:
		leaves = Leaf.objects.filter(content_type=ctype, object_id=instance.id)
		for leaf in leaves:
			leaf.delete()
	except Leaf.DoesNotExist:
		pass

def delete_leaf_children_signal(sender, instance, **kwargs):
	"""
	This is a generic singal to delete related object when a Leaf is deleted.

	"""
	if instance.content_object:
	    instance.content_object.delete()

post_delete.connect(delete_leaf_children_signal, sender=Leaf)