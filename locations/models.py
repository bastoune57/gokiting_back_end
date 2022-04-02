from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class TimePeriod(models.Model):
    """
    Model defining Time periods from a start day to a end day.
    """
    start_date = models.DateField(_('start date'), default=timezone.now, blank=False)
    end_date = models.DateField(_('end date'), null=True, blank=True)
    def __str__(self):
        return "{} - {}".format(self.start_date, self.end_date)

class Location(models.Model):
    """
    Model defining locations as given in Google standard (???)
    """
    city = models.CharField(_('city'), max_length=150, blank=False)
    country = models.CharField(_('country'), max_length=150, blank=False)
    longitude = models.DecimalField(_('longitude'), max_digits=7, decimal_places=4, blank=False, validators=[MinValueValidator(-180.0), MaxValueValidator(+180)])
    latitude = models.DecimalField(_('latitude'), max_digits=6, decimal_places=4, blank=False, validators=[MinValueValidator(-90.0), MaxValueValidator(+90)])
    class Meta:
        unique_together = ("city", "country", "longitude", "latitude")
    def __str__(self):
        return "{} - {}".format(self.city, self.country)

class BaseLocation(models.Model):
    """
    Model defining base locations for a user.
    """
    user = models.ForeignKey(
        'instructors.User',
        on_delete=models.CASCADE,
        blank=False,
        related_name='baselocations',
    )
    location = models.ForeignKey(
        'locations.Location',
        on_delete=models.CASCADE,
        blank=False,
        related_name='baselocations',
    )
    class Meta:
        unique_together = ("user", "location")
    def __str__(self):
        return "{} - {}".format(self.user, self.location)

class TempLocation(models.Model):
    """
    Model defining temporary locations for the users (holidays for instances)
    """
    user = models.ForeignKey(
        'instructors.User',
        on_delete=models.CASCADE,
        blank=False,
        related_name='templocations',
    )
    location = models.ForeignKey(
        'locations.Location',
        on_delete=models.CASCADE,
        blank=False,
        related_name='templocations',
    )
    timeperiod = models.ForeignKey(
        'locations.TimePeriod',
        on_delete=models.CASCADE,
        blank=False,
        related_name='templocations',
    )
    class Meta:
        unique_together = ("user", "location", 'timeperiod')
    def __str__(self):
        return "{} - {}, {}.".format(self.user, self.location, self.timeperiod)