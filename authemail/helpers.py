from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauth2_provider.ext.rest_framework import OAuth2Authentication
from oauthlib.common import generate_token
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import NotFound


def get_token(user):
	try:
		app = Application.objects.get(client_id=settings.OAUTH2_CLIENT_ID)
	except Application.DoesNotExist:
		raise NotFound("The server's oauth2 application is not setup or misconfigured")
	try:
		# AccessToken.objects.filter(user=user, application=app).delete()
		# RefreshToken.objects.filter(user=user, application=app).delete()
		old_access_tokens = AccessToken.objects.filter(
		user=user, application=app)
		old_refresh_tokens = RefreshToken.objects.filter(
		user=user, access_token=old_access_token
		)
	except:
		pass
	else:
		old_access_tokens.delete()
		old_refresh_tokens.delete()

	token = AccessToken.objects.create(user=user, application=app,
	token= generate_token(), expires = timezone.now() + timedelta(days=30),
	scope="read write")
	refresh_token = RefreshToken.objects.create(access_token=token,
	token=generate_token(), user=user, application=app)

	return token.token, refresh_token.token


def delete_token(user):
	try:
		app = Application.objects.get(client_id=OAUTH2_CLIENT_ID)
	except Application.DoesNotExist:
		raise NotFound("The server's oauth2 application is not setup or misconfigured")
	try:
		old_access_tokens = AccessToken.objects.filter(
		user=user, application=app)
		old_refresh_tokens = RefreshToken.objects.filter(
		user=user, access_token=old_access_token
		)
	except:
		pass
	else:
		old_access_tokens.delete()
		old_refresh_tokens.delete()

	return True