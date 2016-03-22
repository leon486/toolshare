from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from toolshare.models.tool import Tool
from toolshare.models.user import User
from toolshare.models.reservation import Reservation
from toolshare.views.base_controller import BaseController
from toolshare.forms.forms_tool import ToolRegistrationForm
from toolshare.forms.forms_tool import BorrowToolForm, ChangeToolForm,ChangeToolAvailabilityForm
import datetime
from datetime import date, timedelta as td
from django.contrib import messages
from django.utils import timezone
import pdb
import pytz
from toolshare.forms.forms_tool import ChangeAvailabilityForm
from toolshare.utils import EmailSender

# Create your views here.
class ToolController(BaseController):
    PAGE_SIZE = 4

    @staticmethod
    @login_required
    def register_tool(request):
        user = User.objects.get(pk=request.user.id)
        if request.method == 'POST':
            pass
            registration_form = ToolRegistrationForm(request.POST,
                                                     request.FILES)
            if registration_form.is_valid():
                # Generate the new-user from the Form
                new_tool = registration_form.save(commit=False)
                new_tool.owner = user
                new_tool.status = 'A'
                if new_tool.shed is not None:
                    new_tool.pickup_location = 'At Shed'
                new_tool.save()
                return redirect('/toolshare/list-owned-tools')
        else:
            # Show the registration-form
            dummy_tool = Tool()
            dummy_tool.pickup_location = user.pickup_location
            registration_form = ToolRegistrationForm(instance=dummy_tool)
            registration_form.fields['shed'].queryset = user.shed_set
        return render(request, 'toolshare/tool-registration.html', {
            'registration_form': registration_form
        })

    @staticmethod
    @login_required
    def find_tool(request):
        user = User.objects.get(pk=request.user.id)
        if request.method == 'GET':
            search_for = request.GET.get('search_for')
            to_date = request.GET.get('to_date')
            from_date = request.GET.get('from_date')

            #Match empty fields to make query work
            if to_date == '':
                to_date = from_date
            if from_date == '':
                from_date = to_date

            #tools = Tool.objects.all()
            tools = Tool.objects.all().exclude(status='D')
            if search_for is not None:
                tools = tools.filter(name__contains=search_for)

            #Find all reservations during the specified dates
            if (to_date is not None and to_date != '') and (from_date is not None and from_date != ''):
                reservations = Reservation.objects.filter(start_date__lte=to_date,
                                                          end_date__gte=from_date,
                                                          status='A')

                #filter them from the results
                for r in reservations:
                    tools = tools.exclude(reservation=r)


            # Only tools in the share-zone
            tools_shared_zone = list()
            for tool in tools:
                owner = User.objects.get(pk=tool.owner.id)
                if owner.share_zone == user.share_zone:
                    tools_shared_zone.append(tool)
            tools = tools_shared_zone
            tool_paginator = Paginator(tools, ToolController.PAGE_SIZE)

            page = request.GET.get('page')
            try:
                tool_page = tool_paginator.page(page)
            except PageNotAnInteger:
                tool_page = tool_paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999),
                # deliver last page of results.
                tool_page = tool_paginator.page(tool_paginator.num_pages)

                search_for = request.GET.get('search_for')

            if search_for is None:
                search_for = ''
            if from_date is None:
                from_date = ''
            if to_date is None:
                to_date = ''

            return render(request, 'toolshare/find_tool.html', {
                'tool_count': len(tools),
                'tool_page': tool_page,
                'search_for': search_for,
                'to_date': to_date,
                'from_date': from_date
            })

        return render(request, 'toolshare/find_tool.html')

    @staticmethod
    @login_required
    def list_owned_tools(request):
        if request.method == 'GET':
            user = User.objects.get(pk=request.user.id)
            user_tools = user.tool_set.all()
            tool_paginator = Paginator(user_tools, ToolController.PAGE_SIZE)

            page = request.GET.get('page')
            try:
                tool_page = tool_paginator.page(page)
            except PageNotAnInteger:
                tool_page = tool_paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999),
                # deliver last page of results.
                tool_page = tool_paginator.page(tool_paginator.num_pages)

            return render(request, 'toolshare/list-owned-tools.html', {
                'tool_page': tool_page,
                'user_tools': user_tools
            })



    def tool_detail(request, tool_id):
        if request.method == 'GET':
            tool = Tool.objects.get(pk=tool_id)

            return render(request, 'toolshare/tool-detail.html', {
                'tool':tool
            })


    @staticmethod
    @login_required
    def change_tool_info(request, tool_id):
        tool = Tool.objects.get(pk= tool_id)
        if request.method == 'POST':
            changeToolInfo = ChangeToolForm(request.POST, request.FILES)
            if changeToolInfo.is_valid():
                newtool = changeToolInfo.save(commit=False)

                #tool.name = newtool.name
                tool.description = newtool.description
                tool.category = newtool.category
                tool.status = newtool.status
                tool.special_instructions = newtool.special_instructions
                tool.pickup_location = newtool.pickup_location
                if "my_picture" in request.FILES:
                    tool.picture = request.FILES['my_picture']
                tool.save()
                return redirect('/toolshare/tool-detail/%s'%tool_id)
        else:
            changeToolInfo = ChangeToolForm(instance=tool)

        return render(request, 'toolshare/tool-info.html',{
            'changeToolInfo' : changeToolInfo,
            'tool':tool
        })

    @staticmethod
    @login_required

    def change_tool_availability(request, tool_id):
        tool = Tool.objects.get(pk= tool_id)
        changeToolAvail_form = ChangeToolAvailabilityForm(requested_tool_id=tool_id)

        if request.method == 'POST':

            Flag = False
            sharedTool = Tool.objects.get(pk = tool_id)
            startdate = request.POST['start_date']
            startDate = datetime.datetime.strptime(startdate, "%m/%d/%Y").replace(tzinfo=pytz.UTC)
            enddate = request.POST['end_date']
            endDate = datetime.datetime.strptime(enddate, "%m/%d/%Y").replace(tzinfo=pytz.UTC)
            # Get all the reservation list of the tool
            tool_reservations = Reservation.objects.filter(tool_id = tool_id)
            for reserve in tool_reservations:
                if reserve.status == 'RP' and reserve.borrower != request.user:
                    if (startDate >= reserve.start_date and startDate <= reserve.end_date) or (startDate <= reserve.start_date and startDate <= reserve.end_date):
                        messages.add_message(request, messages.ERROR, 'You cannot change the tool availability.')
                        Flag = False
                    else:
                        Flag = True
                else:
                    Flag = True
            if Flag:
                for reserve in tool_reservations:
                    if reserve.borrower != request.user:
                        if reserve.status == 'P' or reserve.status == 'A':
                            if (startDate >= reserve.start_date and startDate <= reserve.end_date) or (startDate <= reserve.start_date and startDate <= reserve.end_date):
                                reserve.cancel_msg = 'Your tool reservation has been canceled since the owner changed the availability.'
                                reserve.status = 'C'
                                reserve.save()
                newReservation = Reservation()
                newReservation.status = 'A'
                newReservation.tool = sharedTool
                newReservation.start_date = startDate
                newReservation.end_date = endDate
                newReservation.borrower = request.user
                newReservation.lender = request.user
                newReservation.save()
            return redirect('/toolshare/change-tool-availability/%s'%tool_id)

        else:
            return render(request, 'toolshare/change-tool-availability.html', {'tool': tool,'changeToolAvail_form': changeToolAvail_form,'tool_id': tool_id,'current_date': datetime.datetime.now().strftime('%m/%d/%Y')})

    @staticmethod
    @login_required
    def deactivate_tool(request, tool_id):
        tool = Tool.objects.get(pk=tool_id)
        user = User.objects.get(pk=request.user.id)
        if tool.owner == user:
            tool.status = 'D'
            tool.save()
        return redirect('/toolshare/tool-detail/%s'%tool_id)
        #return render(request, 'toolshare/tool-detail.html',{
        #    'tool':tool
        #})

    @staticmethod
    @login_required
    def change_availability_tool(request, tool_id):
        tool = Tool.objects.get(pk= tool_id)
        user = User.objects.get(pk = request.user.id)
        if request.method == 'POST':
            change_avail_form = ChangeAvailabilityForm(request.POST, requested_tool_id=tool_id)
            if change_avail_form.is_valid():
                new_reservation = change_avail_form.save(commit=False)
                new_reservation.tool = tool
                new_reservation.borrower = user
                if tool.shed is not None:
                    new_reservation.lender = tool.shed.coordinator
                else:
                    new_reservation.lender = user
                new_reservation.status = 'A'

                # Cancel all approved and pending reservations
                reservations = Reservation.objects.filter(
                    tool_id=tool.id,
                    end_date__gt=new_reservation.start_date,
                    start_date__lt=new_reservation.end_date
                )
                for reservation in reservations:
                    if (new_reservation.start_date <= reservation.end_date and
                        new_reservation.end_date >= reservation.start_date):
                        if reservation.status == 'A':
                            reservation.status = 'C'
                            reservation.cancel_msg = 'The owner cancelled this reservation.'
                            EmailSender.send_cancel_request_email(reservation)
                        elif reservation.status == 'P':
                            reservation.status = 'R'
                            reservation.reject_msg = 'The owner rejected this reservation.'
                            EmailSender.send_approve_reject_request_email(reservation)
                        reservation.save()
                # Save the owner-reservation
                new_reservation.save()

                # Display the success message
                a_start = new_reservation.start_date.strftime('%m/%d/%Y')
                a_end = new_reservation.end_date.strftime('%m/%d/%Y')
                messages.add_message(request, messages.SUCCESS, 'You changed the availability of your tool between {0} - {1}. \n"{2}" reservations were cancelled.'.format(a_start, a_end, len(reservations)))
                return redirect('/toolshare/tool-detail/%s' % tool_id)
        else:
            change_avail_form = ChangeAvailabilityForm(requested_tool_id = tool_id)
        return render(request, 'toolshare/change-tool-availability.html', {
            'tool': tool,
            'changeToolAvail_form': change_avail_form,
            'tool_id': tool_id,
            'current_date': datetime.datetime.now().strftime('%m/%d/%Y')
        })

    @staticmethod
    @login_required
    def activate_deactivate_tool(request, tool_id):
        tool = Tool.objects.get(pk=tool_id)
        if tool.status != 'D':
            now = timezone.now()
            reservations = Reservation.objects.filter(tool_id = tool.id, status ="A", start_date__gt = now)
            if len(reservations) > 0:
                messages.add_message(request, messages.WARNING, 'There are pending/approved reservations for the tool. Cancel the reservations first.')
                return redirect('/toolshare/tool-detail/%s'%tool_id)
            tool.status = 'D'
            tool.save()
            return redirect('/toolshare/tool-detail/%s'%tool_id)
        else:
            tool.status = 'A'
            tool.save()
            return redirect('/toolshare/tool-detail/%s'%tool_id)