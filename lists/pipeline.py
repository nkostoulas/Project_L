import datetime
from .models import UserProfile

    # User details pipeline
def user_details(backend, details, response, user=None, *args, **kwargs):
    """Update user details using data from provider."""
    if user:
        if kwargs['is_new']:
            attrs = {'user': user}
            if backend.name == 'facebook':
                fb_data = {
                    'gender': response.get('gender'),
                    'locale': response.get('locale'),
                    'age_range': response.get('age_range'),
                }
                attrs.update(fb_data.items())

            UserProfile.objects.create(
                **attrs
            )
