from django import forms
from toolshare.models.user import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from toolshare.utils import has_numbers, is_valid_name
import re

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    zipcode = forms.CharField(required=True)
    class Meta:
        model = User
        exclude = ['password','groups','user_permissions','is_staff','is_active','is_superuser','last_login','date_joined','share_zone']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        zipcode = cleaned_data.get("zipcode")
        pickup_location = cleaned_data.get("pickup_location")

        if first_name and first_name.strip() == '':
            msg = 'This field is required.'
            self._errors["first_name"] = self.error_class([msg])
            del cleaned_data["first_name"]

        if last_name and last_name.strip() == '':
            msg = 'This field is required.'
            self._errors["last_name"] = self.error_class([msg])
            del cleaned_data["last_name"]

        if first_name and not is_valid_name(first_name):
            msg = 'This field does not allow numbers and special-characters'
            self._errors["first_name"] = self.error_class([msg])
            del cleaned_data["first_name"]

        if last_name and not is_valid_name(last_name):
            msg = 'This field does not allow numbers and special-characters'
            self._errors["last_name"] = self.error_class([msg])
            del cleaned_data["last_name"]

        if zipcode and not re.search(r'^(\d{5}|\d{5}\-\d{4})$', zipcode):
            msg = 'The zip-code should follow the format XXXXX or XXXXX-XXXX: (e.g., 12345 and 12345-6789)'
            self._errors["zipcode"] = self.error_class([msg])
            del cleaned_data["zipcode"]

        if pickup_location and pickup_location.strip() == '':
            msg = 'This field is required.'
            self._errors["pickup_location"] = self.error_class([msg])
            del cleaned_data["pickup_location"]

        return cleaned_data


class ChangeUserPreferencesForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email_remainder_freq', 'pickup_location']
        exclude = ['share_zone']


class ChangeUserForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    zipcode = forms.CharField(required=True)
    class Meta:
        model = User
        exclude = ['username','password','groups','user_permissions','is_staff','is_active','is_superuser','last_login','date_joined','share_zone']

    def __init__(self, *args, **kwargs):
        super(ChangeUserForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangeUserForm, self).clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        zipcode = cleaned_data.get("zipcode")
        pickup_location = cleaned_data.get("pickup_location")

        if first_name and first_name.strip() == '':
            msg = 'This field is required.'
            self._errors["first_name"] = self.error_class([msg])
            del cleaned_data["first_name"]

        if last_name and last_name.strip() == '':
            msg = 'This field is required.'
            self._errors["last_name"] = self.error_class([msg])
            del cleaned_data["last_name"]

        if first_name and not is_valid_name(first_name):
            msg = 'This field does not allow numbers and special-characters'
            self._errors["first_name"] = self.error_class([msg])
            del cleaned_data["first_name"]

        if last_name and not is_valid_name(last_name):
            msg = 'This field does not allow numbers and special-characters'
            self._errors["last_name"] = self.error_class([msg])
            del cleaned_data["last_name"]

        if zipcode and not re.search(r'^(\d{5}|\d{5}\-\d{4})$', zipcode):
            msg = 'The zip-code should follow the format XXXXX or XXXXX-XXXX: (e.g., 12345 and 12345-6789)'
            self._errors["zipcode"] = self.error_class([msg])
            del cleaned_data["zipcode"]

        if pickup_location and pickup_location.strip() == '':
            msg = 'This field is required.'
            self._errors["pickup_location"] = self.error_class([msg])
            del cleaned_data["pickup_location"]

        return cleaned_data
