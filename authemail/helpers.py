from rest_framework import permissions
from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauth2_provider.ext.rest_framework import OAuth2Authentication
from oauthlib.common import generate_token
from .settings import OAUTH2_CLIENT_ID
from django.utils import timezone
from datetime import timedelta

def get_token(user):
	try:
		app = Application.objects.get(client_id=OAUTH2_CLIENT_ID)
		print app
	except Application.DoesNotExist:
		return Response({
		"detail": "The server's oauth2 application is not setup or misconfigured"
		}, status=status.HTTP_501_NOT_IMPLEMENTED)

	try:
		AccessToken.objects.filter(user=user, application=app).delete()
		RefreshToken.objects.filter(user=user, application=app).delete()
	except:
		pass

	token = AccessToken.objects.create(user=user, application=app,
	token=generate_token(), expires=timezone.now() + timedelta(days=25),
	scope="read write")
	refresh_token = RefreshToken.objects.create(access_token=token,
	token=generate_token(), user=user, application=app)

	return token.token, refresh_token.token