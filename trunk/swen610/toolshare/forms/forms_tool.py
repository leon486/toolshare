from django import forms
from toolshare.models.tool import Tool
from toolshare.models.reservation import Reservation
from toolshare.forms.widgets import DateTimePickerField
import datetime
from django.utils import timezone


class ToolRegistrationForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = '__all__'
        exclude = ['status', 'owner']

    def __init__(self, *args, **kwargs):
        super(ToolRegistrationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ToolRegistrationForm, self).clean()
        category = cleaned_data.get("category")
        pickup_location = cleaned_data.get("pickup_location")

        if pickup_location and pickup_location.strip() == '':
            msg = 'This field is required.'
            self._errors["pickup_location"] = self.error_class([msg])
            del cleaned_data["pickup_location"]

        if category and category.strip() == '':
            msg = 'This field is required.'
            self._errors["category"] = self.error_class([msg])
            del cleaned_data["category"]
        return cleaned_data

class BorrowToolForm(forms.ModelForm):
    start_date = DateTimePickerField(initial=datetime.datetime.now())
    end_date = DateTimePickerField(initial=datetime.datetime.now())

    class Meta:
        model = Reservation
        exclude = ['status', 'reject_msg', 'cancel_msg', 'lender', 'borrower',
                   'tool']

    def __init__(self, *args, **kwargs):
        self.requested_tool_id = kwargs.pop("requested_tool_id")
        super(BorrowToolForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(BorrowToolForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError(
                    "End-date must be greater than Start-date")

            # Get all the approved reservations
            reservations = Reservation.objects.filter(
                status = 'A',
                tool_id=self.requested_tool_id,
                end_date__gt=start_date,
                start_date__lt=end_date
            )
            for reservation in reservations:
                if (start_date <= reservation.end_date and
                    end_date >= reservation.start_date):
                    conflict_start = reservation.start_date.strftime('%m/%d/%Y')
                    conflict_end = reservation.end_date.strftime('%m/%d/%Y')
                    error_msg = ('Your request conflicts with '
                                 'reservation [{0} - {1}]').format(conflict_start, conflict_end)
                    raise forms.ValidationError(error_msg)
        return cleaned_data


class ChangeToolAvailabilityForm(forms.ModelForm):
    start_date = DateTimePickerField(initial=datetime.datetime.now())
    end_date = DateTimePickerField(initial=datetime.datetime.now())

    class Meta:
        model = Reservation
        exclude = ['status', 'reject_msg', 'cancel_msg', 'lender', 'borrower',
                   'tool','request_msg']

    def __init__(self, *args, **kwargs):
        self.requested_tool_id = kwargs.pop("requested_tool_id")
        super(ChangeToolAvailabilityForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangeToolAvailabilityForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError(
                    "End-date must be greater than Start-date")

            # Get all the approved reservations
            reservations = Reservation.objects.filter(
                status = 'A',
                tool_id=self.requested_tool_id,
                end_date__gt=start_date,
                start_date__lt=end_date
            )
            for reservation in reservations:
                if (start_date <= reservation.end_date and
                    end_date >= reservation.start_date):
                    conflict_start = reservation.start_date.strftime('%m/%d/%Y')
                    conflict_end = reservation.end_date.strftime('%m/%d/%Y')
                    error_msg = ('Your request conflicts with '
                                 'reservation [{0} - {1}]').format(conflict_start, conflict_end)
                    raise forms.ValidationError(error_msg)
        return cleaned_data


class ChangeToolForm(forms.ModelForm):
    #forms.
    #name = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    my_picture = forms.ImageField(required=False)

    class Meta:
        model = Tool
        fields = '__all__'
        exclude = ['status', 'owner', 'name', 'picture']

    def __init__(self, *args, **kwargs):
        super(ChangeToolForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangeToolForm, self).clean()
        category = cleaned_data.get("category")
        pickup_location = cleaned_data.get("pickup_location")

        if pickup_location and pickup_location.strip() == '':
            msg = 'This field is required.'
            self._errors["pickup_location"] = self.error_class([msg])
            del cleaned_data["pickup_location"]

        if category and category.strip() == '':
            msg = 'This field is required.'
            self._errors["category"] = self.error_class([msg])
            del cleaned_data["category"]
        return cleaned_data


class ChangeAvailabilityForm(forms.ModelForm):
    start_date = DateTimePickerField(initial=datetime.datetime.now())
    end_date = DateTimePickerField(initial=datetime.datetime.now())

    class Meta:
        model = Reservation
        exclude = ['status', 'reject_msg', 'cancel_msg', 'lender', 'borrower',
                   'tool','request_msg']

    def __init__(self, *args, **kwargs):
        self.requested_tool_id = kwargs.pop("requested_tool_id")
        super(ChangeAvailabilityForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangeAvailabilityForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        current_date = timezone.now()
        tool = Tool.objects.get(pk=self.requested_tool_id)
        owner_id = tool.owner.id

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError(
                    "End-date must be greater than Start-date")

            # Check if the owner posses the tool
            in_progress_reservations = Reservation.objects.filter(
                status='A',
                tool_id=self.requested_tool_id,
                start_date__lt=start_date,
                end_date__gt=start_date,
            ).exclude(lender_id=owner_id)

            if len(in_progress_reservations):
                error_msg = ('The tool is already borrowed. You need '
                             'to have the tool in your possession')
                raise forms.ValidationError(error_msg)
        return cleaned_data

#
#
# my-start > p-start

# my-start < p-end  +
# my-end > p-start  +

# my-end > p-end

# my-start < p-start

# my-start < p-end  +
# my-end > p-start  +

# my-end > p-end

# my-start < p-start

# my-start < p-end  +
# my-end > p-start  +

# my-end < p-end



