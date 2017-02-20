import datetime, json
from urllib.request import Request, urlopen
from .models import UserProfile

    # User details pipeline
def user_details(backend, details, response, user=None, *args, **kwargs):
    """Update user details using data from provider."""
    if user:
        if kwargs['is_new']:
            attrs = {'user': user}
            if backend.name == 'facebook':
                fb_data = {
                    'fbid': response.get('id'),
                    'gender': response.get('gender'),
                    'locale': response.get('locale'),
                    'age_range': response.get('age_range'),
                }
                attrs.update(fb_data.items())

            UserProfile.objects.create(
                **attrs
            )

def user_email(strategy, *args, **kwargs):
    if not kwargs['is_new']:
        return

    user = kwargs['user']
    fbuid = kwargs['response']['id']
    access_token = kwargs['response']['access_token']
    url = u'https://graph.facebook.com/{0}/' \
          u'?fields=email' \
          u'&access_token={1}'.format(
        fbuid,
        access_token,
    )
    request = Request(url)
    email = json.loads(urlopen(request).read().decode('utf-8')).get('email')
    user.email = email
    user.save()
