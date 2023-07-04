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
    time = models.DateTimeField()

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE
    )


class Station(models.Model):
    name = models.CharField(max_length=32)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return self.name


class Trace(models.Model):
    path = models.CharField(max_length=256)  # путь будет начинаться с базовой директории локаций
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event'
    )

    station = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        related_name='station'
    )
