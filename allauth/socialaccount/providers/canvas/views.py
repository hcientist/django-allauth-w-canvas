import requests

from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import CanvasProvider


class CanvasOAuth2Adapter(OAuth2Adapter):
    provider_id = CanvasProvider.id

    settings = app_settings.PROVIDERS.get(provider_id, {})
    provider_base_url = settings.get("CANVAS_URL", "")

    access_token_url = "{0}/login/oauth2/token/".format(provider_base_url)
    authorize_url = "{0}/login/oauth2/auth".format(provider_base_url)
    profile_url = "{0}/api/v1/users/self/profile".format(provider_base_url)

    def complete_login(self, request, app, token, **kwargs):
        print(token)
        resp = requests.get(
            self.profile_url, headers={"Authorization": "Bearer " + token.token}
        )
        resp.raise_for_status()
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(CanvasOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(CanvasOAuth2Adapter)
