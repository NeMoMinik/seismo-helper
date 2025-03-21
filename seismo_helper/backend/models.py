from django.db import models


class Corporation(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    corporation = models.ForeignKey(
        Corporation,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Event(models.Model):
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    magnitude = models.FloatField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    name = models.CharField(max_length=32)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE
    )
    # traces = Trace


class Station(models.Model):
    name = models.CharField(max_length=32)
    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)
    z = models.FloatField(null=True, blank=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Trace(models.Model):
    path = models.CharField(max_length=256)
    timedelta = models.IntegerField(default=5)
    p_peak = models.IntegerField(blank=True, null=True)
    s_peak = models.IntegerField(blank=True, null=True)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='traces'
    )

    station = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        related_name='traces'
    )

    def __str__(self):
        return self.path


class Channel(models.Model):
    path = models.CharField(max_length=128)
    trace = models.ForeignKey(
        Trace,
        on_delete=models.CASCADE,
        related_name="channels"
    )

    def __str__(self):
        return self.path
