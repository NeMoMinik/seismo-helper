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
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    magnitude = models.FloatField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    name = models.CharField(max_length=32)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE
    )


class Station(models.Model):
    name = models.CharField(max_length=32)
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    z = models.FloatField(null=True)

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Trace(models.Model):
    path = models.CharField(max_length=256)
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
