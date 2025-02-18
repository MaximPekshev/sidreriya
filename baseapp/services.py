
import uuid

def get_uuid():
	return str(uuid.uuid4().fields[0])

def get_image_name_by_slug(instance, filename):
	new_name = ('%s' + '.' + filename.split('.')[-1]) % instance.slug
	return new_name