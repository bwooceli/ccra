from django.db import models

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


from ccra.base_models import BaseCcraModel
from race_organization.models import RaceOrganization
from race_car.models import Car


class GrandPrixInvitation(BaseCcraModel):
    """
    The Grand Prix Invitation lets organizations invite racers to register
    for a Grand Prix event with a special invitation code.  The invitation code
    is used to register the racer for for a published session.
    """

    grandprix = models.ForeignKey("GrandPrix", on_delete=models.CASCADE)
    code = models.CharField(
        max_length=255, unique=True, help_text=_("Invitation code for this Grand Prix")
    )
    lock_date = models.DateField(
        null=True,
        blank=True,
        help_text=_("Date after which the invitation code will no longer be valid"),
    )

    password = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Optionally set a password in addition to the invitation code"), )

    status = models.CharField(
        max_length=255,
        choices=(
            ("active", _("Active")),
            ("locked", _("Locked")),
            ("inactive", _("Inactive")),
        ),
        default="active",
    )

    def save(self, *args, **kwargs):
        # if the unique code is not at least 25 characters, throw a validation error and don't save
        if len(self.code) < 13:
            raise ValidationError(
                _(
                    "Invitation code must be at least 13 characters long, four words recommended"
                )
            )
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ["grandprix", "code"]


class GrandPrix(BaseCcraModel):
    """GrandPrix model
    A race event is a collection of races, like "Pack 3456 - 2023 Race Day"
    """

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    slug = models.SlugField(max_length=255)

    organization = models.ForeignKey(RaceOrganization, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # add unique together constraint for slug and organization
    class Meta:
        unique_together = ["slug", "organization"]


class RaceSession(BaseCcraModel):
    """
    A race session is a collection of Heats associated to a GrandPrix
    such as Scouts Qualifying, Scouts Championship, Outlaw Division, etc
    """

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    event = models.ForeignKey("GrandPrix", on_delete=models.CASCADE)

    position_podiums = models.IntegerField(default=4)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # @property
    # def heats(self):
    #     return self.heat_set.all().count()

    class Meta:
        unique_together = ["slug", "event"]

    # return an ordered list of heat results by time_result
    # def heat_results(self):
    #     return self.heatresult_set.all().order_by("time_result")

    # def register_car_for_race(self, car):
    #     # check if car is already registered
    #     if self.careventregistration_set.filter(car=car).exists():
    #         return False

    #     # get the next registration number
    #     next_registration_number = self.careventregistration_set.all().count() + 1

    #     # register the car
    #     car_event_registration = GrandPrixRegistration.objects.create(
    #         car=car, event=self.event, registration_number=next_registration_number
    #     )

    #     return car_event_registration

    # return an ordered list of cars by their average time_result
    # def car_results(self):
    #     car_results = {}
    #     for heat_result in self.heat_results():
    #         car = heat_result.car
    #         if car not in car_results:
    #             car_results[car] = []
    #         car_results[car].append(heat_result.time_result)

    #     # calculate average time
    #     for car in car_results:
    #         car_results[car] = sum(car_results[car]) / len(car_results[car])

    #     # sort by time
    #     car_results = sorted(car_results.items(), key=lambda item: item[1])

    #     return car_results


class SessionHeat(BaseCcraModel):
    """
    A heat collects results of car results on a track
    """

    session = models.ForeignKey("RaceSession", on_delete=models.CASCADE)
    heat_number = models.IntegerField()
    completed_timestamp = models.DateTimeField(blank=True, null=True)
    timer_correlation_uuid = models.UUIDField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.heat_number:
            self.heat_number = self.session.sessionheat_set.all().count() + 1
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ["heat_number", "session"]


class SessionHeatResult(BaseCcraModel):
    """
    A heat result is a result of a car in a heat
    """

    heat = models.ForeignKey("SessionHeat", on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    lane_number = models.IntegerField()
    time_result = models.FloatField()


class GrandPrixRegistration(BaseCcraModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    event = models.ForeignKey("GrandPrix", on_delete=models.CASCADE)
    registration_number = models.IntegerField()

    checked_in = models.BooleanField(default=False)
    checked_in_timestamp = models.DateTimeField(blank=True, null=True)

    weight = models.FloatField(blank=True, null=True)
    weight_official = models.BooleanField(default=False)

    official_signoff_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="official_signoff_by",
    )
