import uuid

from django.db import models

# django auth user model
from django.contrib.auth.models import User

# import django translation helpers
from django.utils.translation import gettext_lazy as _


# base class that has a guid field as the primary key and sets the auto_admin_reg to True
class BaseRaceDayModel(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    auto_admin_reg = True

    class Meta:
        abstract = True


# a selection of the 15 most common colors in ROYGBIV format/order, includes brown
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


class CarMaker(BaseRaceDayModel):
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
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.user:
            return self.user.username
        else:
            return "Unknown"

    # override save method to ensure values are set for first and last name
    def save(self, *args, **kwargs):
        if not self.user:
            if not self.first_name or not self.last_name:
                raise ValueError(
                    _("Either a user or first and last name must be provided")
                )
            self.first_name = self.first_name.strip()
            self.last_name = self.last_name.strip()


class Car(BaseRaceDayModel):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey("CarMaker", on_delete=models.SET_NULL, null=True)
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


class RaceEvent(BaseRaceDayModel):
    """RaceEvent model
    A race event is a collection of races
    """

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Race(BaseRaceDayModel):
    """
    A race is a collection of Heats associated to a RaceEvent
    """

    title = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    event = models.ForeignKey("RaceEvent", on_delete=models.CASCADE)

    position_podiums = models.IntegerField(default=4)

    def __str__(self):
        return self.title

    @property
    def heats(self):
        return self.heat_set.all().count()

    # return an ordered list of heat results by time_result
    def heat_results(self):
        return self.heatresult_set.all().order_by("time_result")

    def register_car_for_race(self, car):
        # check if car is already registered
        if self.careventregistration_set.filter(car=car).exists():
            return False

        # get the next registration number
        next_registration_number = self.careventregistration_set.all().count() + 1

        # register the car
        car_event_registration = CarEventRegistration.objects.create(
            car=car, event=self.event, registration_number=next_registration_number
        )

        return car_event_registration

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


class Heat(BaseRaceDayModel):
    """
    A heat collects results of car results on a track
    """

    race = models.ForeignKey("Race", on_delete=models.CASCADE)
    number = models.IntegerField()
    completed_timestamp = models.DateTimeField(blank=True, null=True)
    timer_correlation_uuid = models.UUIDField(blank=True, null=True)


class HeatResult(BaseRaceDayModel):
    """
    A heat result is a result of a car in a heat
    """

    heat = models.ForeignKey("Heat", on_delete=models.CASCADE)
    car = models.ForeignKey("Car", on_delete=models.CASCADE)
    lane_number = models.IntegerField()
    time_result = models.FloatField()

    @property
    def car_name(self):
        return self.car.name

    @property
    def heat_place(self):
        return self.heat.heatresult_set.all().order_by("time_result").index(self) + 1


class CarEventRegistration(BaseRaceDayModel):
    car = models.ForeignKey("Car", on_delete=models.CASCADE)
    event = models.ForeignKey("RaceEvent", on_delete=models.CASCADE)
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

    def __str__(self):
        return f"{self.car.name} - {self.event.title} - {self.division.name}"
