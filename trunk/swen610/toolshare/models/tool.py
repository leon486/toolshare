from django.db import models
from toolshare.models.base_model import BaseModel
from toolshare.models.user import User
from toolshare.models.shed import Shed
from localflavor.us import models as us_models
from datetime import datetime


def generate_filename(instance, filename):
    """Generate the path of the tool-picture"""
    return 'users/{email}/tools/{stamp}-{file}'.format(email=instance.owner.email,
                                                       stamp=datetime.now().timestamp(),
                                                       file=filename)


class Tool(BaseModel):
    TOOL_STATUS_TYPE = (
        ('A', 'Available'),
        ('U', 'Unavailable'),
        ('D', 'Deactivated'),
        ('B', 'Borrowed'),      #Someone else has the tool
        ('R', 'Returned'),      #The tool is returned but pending
        ('L', 'Lost')           #The is was returned but cannot be acknowledged
    )
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=20, blank=False)
    picture = models.ImageField(upload_to=generate_filename)
    status = models.CharField(max_length=10, choices=TOOL_STATUS_TYPE, default='A', null=False)
    special_instructions = models.TextField(null=True, blank=True)
    pickup_location = models.CharField(max_length=100, null=False)
    owner = models.ForeignKey(User)
    shed = models.ForeignKey(Shed, null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.name, self.owner)

    def get_status_description(self):
        return {k:v for k,v in Tool.TOOL_STATUS_TYPE}[self.status]