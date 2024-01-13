from django.db import models

from ccra.base_models import BaseCcraModel
from grand_prix.models import GrandPrix


class TrackTimerManufacturer(BaseCcraModel):
    """TrackTimerManufacturer model
    Sample
        Name: Microwizard
        Website: https://www.microwizard.com/
        Phone Number: 1-800-999-9999
        Description: Microwizard is a company that makes track gates for craft car tracks
    """

    name = models.CharField(max_length=100)
    website = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class TrackTimer(BaseCcraModel):
    """TrackTimer model
    Sample
        Model: K3
        Version: 1.0
        Manufacturer: Microwizard

    output_file will store raw heat results from the track gate to a csv file in the track_output directory
    """

    manufacturer = models.ForeignKey(
        "TrackTimerManufacturer", on_delete=models.CASCADE, related_name="track_timers"
    )
    model = models.CharField(max_length=100)
    version = models.CharField(max_length=100)
    lane_count = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    picture = models.ImageField(upload_to="track_gate_pictures", blank=True, null=True)

    output_file = models.CharField(max_length=255, blank=True, null=True)

    sample_result_string = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default='@A=1.758# B=1.392" C=1.086! D=0.000  E=0.000  F=0.000',
    )

    # set uniquetogether to manufacturer, model, version
    class Meta:
        unique_together = ("manufacturer", "model", "version")

    def __str__(self):
        return f"{self.manufacturer} {self.model} {self.version}"


class GrandPrixRawDataLog(BaseCcraModel):
    """Raw data log for a grand prix event"""

    event = models.ForeignKey(GrandPrix, on_delete=models.CASCADE)
    correlation_id = models.UUIDField()
    raw_data = models.TextField()

    source_ip = models.CharField(max_length=100, blank=True, null=True)
