from django.db import models

# Create your models here.
class Track(models.Model):
    name = models.CharField(max_length=100)
    lane_count = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name