import datetime
from .models import UserProfile

    # User details pipeline
def user_details(backend, details, response, user=None, *args, **kwargs):
    """Update user details using data from provider."""
    if user:
        if kwargs['is_new']:
            attrs = {'user': user}
            # I am using also Twitter backend, so I am checking if It's FB
            # or Twitter. Might be a better way of doing this
            if backend.name == 'facebook':
                # We should check values before this, but for the example
                # is fine
                fb_data = {
                    'gender': response.get('gender'),
                    'locale': response.get('locale'),
                    'age_range': response.get('age_range'),
                }
                attrs.update(fb_data.items())

            UserProfile.objects.create(
                **attrs
            )
