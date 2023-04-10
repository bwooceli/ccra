from django.db import models


class TrackGateManufacturer(models.Model):
    """TrackGateManufacturer model
    Sample
        Name: Microwizard
        Website: https://www.microwizard.com/
        Phone Number: 1-800-999-9999
        Description: Microwizard is a company that makes track gates for pinewood derby tracks
    """

    name = models.CharField(max_length=100)
    website = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class TrackGate(models.Model):
    """TrackGate model
    Sample
        Model: K3
        Version: 1.0
        Manufacturer: Microwizard

    output_file will store raw heat results from the track gate to a csv file in the track_output directory
    """

    manufacturer = models.CharField(max_length=100)
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
        default="@A=9.999! B=9.999  C=9.999  D=0.000  E=0.000  F=0.000  \r\n",
    )

    # set uniquetogether to manufacturer, model, version
    class Meta:
        unique_together = ("manufacturer", "model", "version")

    def __str__(self):
        return self.name
