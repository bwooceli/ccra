"""ccra URL Configuration"""


from django.contrib import admin

from django.contrib.auth import views as auth_views

from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # use grand_prix as the base url for the root
    path("", include("grand_prix.urls")),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    # other URL patterns for your project
]
