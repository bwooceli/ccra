from ccra.base_models import BaseCcraModel

from django.db import models

# import django translation helpers
from django.utils.translation import gettext_lazy as _


class RaceOrganization(BaseCcraModel):
    """The organizing group for a race event (district, pack, troop, etc)"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    parent_organization = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="child_organizations",
        help_text=_("Parent organization for this organization"),
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super().save(*args, **kwargs)
