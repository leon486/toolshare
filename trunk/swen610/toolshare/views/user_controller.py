from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from toolshare.models.user import User
from toolshare.models.sharezone import ShareZone
from toolshare.views.base_controller import BaseController
from toolshare.forms.forms_user import ChangeUserPreferencesForm, ChangeUserForm
from toolshare.forms.forms_user import UserRegistrationForm


class UserController(BaseController):

    @staticmethod
    def register_user(request):
        if request.method == 'POST':
            registration_form = UserRegistrationForm(request.POST)
            if registration_form.is_valid():
                # Generate the new-user from the Form
                new_user = registration_form.save(commit=False)

                # Get the user's share_zone
                query_result = ShareZone.objects.filter(zipcode=new_user.zipcode)
                if len(query_result) == 1:
                    share_zone = query_result[0]
                else:
                    # Create a new ShareZone
                    share_zone = ShareZone(zipcode=new_user.zipcode)
                    share_zone.save()
                new_user.share_zone = share_zone

                new_user.save()
                return redirect('/toolshare/login')
        else:
            # Show the registration-form
            registration_form = UserRegistrationForm()

        return render(request, 'toolshare/user-registration.html',{
            'registration_form': registration_form
        })

    @staticmethod
    ##DEAD CODE##
    def login_user(request):

        """
        This method is deprecated. Although it works, it is not integrated
        with the django-session and authentication modules.
        """
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # Create a session
                login(request, user)

                # Redirect to the my_account page
                return redirect('/toolshare/my_account/')
            else:
                # The credentials are invalid
                # Show the login-form Again
                auth_form = AuthenticationForm()
                return render(request, 'toolshare/login.html', {
                    'auth_form': auth_form
                })
        else:
            # GET method
            # Show the login-form
            auth_form = AuthenticationForm()
            return render(request, 'toolshare/login.html', {
                'auth_form': auth_form
            })

    @staticmethod
    @login_required
    def my_account(request):
        return render(request, 'toolshare/my_account.html')

    @staticmethod
    @login_required
    def personal_info(request):
        return render(request, 'toolshare/personal_info.html')

    @staticmethod
    @login_required
    def change_user_preferences(request):
        if request.method == 'POST':
            preferences_form = ChangeUserPreferencesForm(request.POST)

            if preferences_form.is_valid():
                pickup_location = request.POST['pickup_location']
                email_remainder_freq = request.POST['email_remainder_freq']
                user = User.objects.get(pk = request.user.id)
                user.pickup_location = pickup_location
                user.email_remainder_freq = email_remainder_freq
                user.save()

                #preferences_form.save()
                # Redirect to the my_account page
                return redirect('/toolshare/my_account')
        else:
            # Show the registration-form
            user = User.objects.get(pk = request.user.id)

            preferences_form = ChangeUserPreferencesForm(instance=user)

        return render(request, 'toolshare/personal-info-preferences.html',{
            'preferences_form': preferences_form
        })

    @staticmethod
    @login_required
    def change_personal_info(request):
        if request.method == 'POST':
            changeUserForm = ChangeUserForm(request.POST)
            if changeUserForm.is_valid():
                # Generate the new-user from the Form
                #user = changeUserForm.save(commit=False)
                user = User.objects.get(pk=request.user.id)

                # From the POST
                pickup_location = request.POST['pickup_location']
                email_remainder_freq = request.POST['email_remainder_freq']
                address_line = request.POST['address_line']
                zipcode = request.POST['zipcode']
                email = request.POST['email']
                city = request.POST['city']
                state = request.POST['state']
                phone = request.POST['phone']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']

                # Save them in the user
                user.pickup_location = pickup_location
                user.email_remainder_freq = email_remainder_freq
                user.email = email
                user.address_line = address_line
                user.zipcode = zipcode
                user.city = city
                user.state = state
                user.phone = phone
                user.first_name = first_name
                user.last_name = last_name
                # Get the user's share_zone
                query_result = ShareZone.objects.filter(zipcode=user.zipcode)
                if len(query_result) == 1:
                    share_zone = query_result[0]
                else:
                    # Create a new ShareZone
                    share_zone = ShareZone(zipcode=user.zipcode)
                    share_zone.save()
                user.share_zone = share_zone

                user.save()
                return redirect('/toolshare/my_account')
        else:
            user = User.objects.get(pk=request.user.id)
            # Show the registration-form
            changeUserForm = ChangeUserForm(instance=user)
        return render(request, 'toolshare/personal_info.html',{
            'changeUserForm': changeUserForm
        })