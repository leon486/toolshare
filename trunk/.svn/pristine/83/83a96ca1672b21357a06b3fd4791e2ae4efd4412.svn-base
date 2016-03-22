from django import forms
from toolshare.models.shed import Shed
import re


class ShedForm(forms.ModelForm):
    #address = forms.CharField(required=True)
    #zipcode = forms.CharField(required=True)
    #city = forms.CharField(required=True)
    #state = forms.CharField(required=True)
    #coordinator = forms.CharField(required=True)
    class Meta:
        model = Shed
        exclude = ['coordinator']

    def __init__(self, *args, **kwargs):
        super(ShedForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ShedForm, self).clean()
        address = cleaned_data.get("address")
        city = cleaned_data.get("city")
        zipcode = cleaned_data.get("zipcode")

        if address and address.strip() == '':
            msg = 'This field is required.'
            self._errors["address"] = self.error_class([msg])
            del cleaned_data["address"]

        if city and city.strip() == '':
            msg = 'This field is required.'
            self._errors["city"] = self.error_class([msg])
            del cleaned_data["city"]

        if zipcode and not re.search(r'^(\d{5}|\d{5}\-\d{4})$', zipcode):
            msg = 'The zip-code should follow the format XXXXX or XXXXX-XXXX: (e.g., 12345 and 12345-6789)'
            self._errors["zipcode"] = self.error_class([msg])
            del cleaned_data["zipcode"]

        return cleaned_data
