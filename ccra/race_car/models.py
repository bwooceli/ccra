from ccra.base_models import BaseCcraModel


# import django translation helpers
from django.utils.translation import gettext_lazy as _
from django.db import models

from django.contrib.auth.models import User

# a selection of the most common colors for cars
COLOR_CHOICES = (
    ("BLU", _("Blue")),
    ("BRN", _("Brown")),
    ("GLD", _("Gold")),
    ("GRN", _("Green")),
    ("ORG", _("Orange")),
    ("PNK", _("Pink")),
    ("PUR", _("Purple")),
    ("RED", _("Red")),
    ("SLV", _("Silver")),
    ("YLW", _("Yellow")),
    ("BLK", _("Black")),
    ("WHT", _("White")),
    ("GRY", _("Gray")),
)


class CarMaker(BaseCcraModel):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    # recursive relationship to self
    helper = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="helpers",
        help_text=_("Helper for this car maker"),
    )

    def __str__(self):
        # return the first and last name if they exist, otherwise return the username
        maker_str = None
        if self.first_name and self.last_name:
            maker_str = f"{self.first_name} {self.last_name}"
        elif self.user:
            maker_str = self.user.username

        # check if the user has a helper
        if self.helper:
            maker_str = f"{maker_str} (Helper: {self.helper})"

        return maker_str

    # override save method to ensure values are set for first and last name
    def save(self, *args, **kwargs):
        if not self.user:
            if not self.first_name or not self.last_name:
                raise ValueError(
                    _("Either a user or first and last name must be provided")
                )
            self.first_name = self.first_name.strip()
            self.last_name = self.last_name.strip()


class Car(BaseCcraModel):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        "CarMaker", on_delete=models.SET_NULL, blank=True, null=True
    )
    primary_color = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=COLOR_CHOICES,
    )
    accent_color = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=COLOR_CHOICES,
    )
    description = models.TextField(
        blank=True, null=True, help_text=_("Description of the car, be specific")
    )

    def __str__(self):
        return self.name

    # override save method to clean up name before saving
    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super().save(*args, **kwargs)
