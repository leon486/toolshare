from django.db import models
from toolshare.models.base_model import BaseModel
from toolshare.models.user import User
from toolshare.models.tool import Tool
from toolshare.models.shed import Shed
from localflavor.us import models as us_models

class Reservation(BaseModel):
    STATUS_TYPE = (
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
        ('C', 'Cancelled'),
        ('RP', 'Return Pending'),
        ('RA', 'Return Acknowledged'),
        ('RD', 'Not Returned (Lost tool)')
    )
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    status = models.CharField(max_length=2, choices=STATUS_TYPE, default='P')
    request_msg = models.CharField(max_length=100, null=True, blank=True)
    reject_msg = models.CharField(max_length=100, null=True, blank=True)
    cancel_msg = models.CharField(max_length=100, null=True, blank=True)
    lender = models.ForeignKey(User, related_name='lender')
    borrower = models.ForeignKey(User, related_name='borrower')
    tool = models.ForeignKey(Tool)

    def __str__(self):
        return u'{0} - {1} - lender: {2} - borrower: {3}'.format(self.id, self.get_status_description(), self.lender, self.borrower)

    def get_status_description(self):
        return {k: v for k, v in Reservation.STATUS_TYPE}[self.status]

    def is_approved(self):
        return self.status == 'A'

