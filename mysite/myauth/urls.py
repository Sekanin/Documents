from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    logout_view,
    AboutMeView, RegisterView,
    get_cookie_view, set_cookie_view,
    get_session_view, set_session_view
)

app_name = "myauth"

urlpatterns = [
    path("login/",
         LoginView.as_view(
             template_name="myauth/login.html",
             redirect_authenticated_user=True,
         ),
         name="login"),

    path("register/", RegisterView.as_view(), name="register"),  # Changé ici
    path("logout/", logout_view, name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),

    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),

    path("session/get/", get_session_view, name="session-get"),
    path("session/set/", set_session_view, name="session-set"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)