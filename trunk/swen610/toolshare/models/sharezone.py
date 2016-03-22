from django.db import models
from toolshare.models.base_model import BaseModel

class ShareZone(BaseModel):
    zipcode = models.CharField(max_length=5, null=False, unique=True)

    def __str__(self):
        return self.zipcode
