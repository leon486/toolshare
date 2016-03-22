from django.db import models
from django.contrib.auth.models import User
from toolshare.models.base_model import BaseModel
from toolshare.models.sharezone import ShareZone
from toolshare.models.reservation import Reservation
from localflavor.us import models as us_models


class User(User):
    class Meta:
        app_label = 'toolshare'

    REMAINDER_FREQ_TYPE = (
        ('D', 'Every day'),
        ('W', 'Once a week'),
        ('M', 'Once a month'),
        ('N', 'Never')
    )
    address_line = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=20, null=False)
    state = us_models.USStateField(null=False)
    zipcode = models.IntegerField(max_length=5, null=False)
    phone = us_models.PhoneNumberField(null=True, blank=True)
    email_remainder_freq = models.CharField(max_length=1, choices=REMAINDER_FREQ_TYPE, default='D')
    pickup_location = models.CharField(max_length=100, null=False)
    share_zone = models.ForeignKey(ShareZone)

    def __str__(self):
        return '{first} {last}'.format(first=self.first_name,
                                       last=self.last_name)

    def _pending_requests(self):
        reservation = Reservation.objects.filter(lender_id=self.id, status__in=['RP','P'])
        return reservation.count()

    pending_requests = property(_pending_requests)