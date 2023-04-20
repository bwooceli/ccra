from django.urls import path

from . import views

# url patterns for the grand_prix app
urlpatterns = [
    path("", views.landing_page, name="landing_page"),
]
