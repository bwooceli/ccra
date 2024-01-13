from django.contrib import admin
from django.apps import apps

# Generic register everything else to admin
app_for_admin = apps.get_app_config("race_car")
for model_name, model in app_for_admin.models.items():
    if not admin.site.is_registered(model) and "auto_admin_reg" in dir(model):
        if model.auto_admin_reg:
            admin.site.register(model)