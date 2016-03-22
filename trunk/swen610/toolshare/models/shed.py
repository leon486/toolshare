from django.db import models
from toolshare.models.base_model import BaseModel
from toolshare.models.user import User
from localflavor.us import models as us_models

class Shed(BaseModel):
    address = models.CharField(max_length=50, null=False,blank=False)
    zipcode = models.CharField(max_length=5, null=False)
    city = models.CharField(max_length=20, null=False)
    state = us_models.USStateField(null=False)
    coordinator = models.ForeignKey(User)

    def __str__(self):
        return '-'.join([self.address, self.city, self.state, self.zipcode])

    def to_string(self):
        return "%s %s, %s %s" % (self.address,
                                 self.city,
                                 self.state,
                                 self.zipcode)