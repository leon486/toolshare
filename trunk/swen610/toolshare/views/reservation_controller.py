from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from toolshare.models.tool import Tool
from toolshare.models.user import User
from toolshare.models.reservation import Reservation
from toolshare.views.base_controller import BaseController
from toolshare.forms.forms_tool import BorrowToolForm
from toolshare.utils import EmailSender
import datetime
from datetime import date, timedelta as td
from django.contrib import messages
from django.utils import timezone

# Create your views here.
class ReservationController(BaseController):
    PAGE_SIZE_BORROWED_TOOLS = 4

    @staticmethod
    @login_required
    def borrow_tool(request, tool_id):
        user = User.objects.get(pk=request.user.id)
        tool = Tool.objects.get(pk=tool_id)
        if request.method == 'POST':
            borrow_form = BorrowToolForm(request.POST, requested_tool_id=tool_id)

            if borrow_form.is_valid():
                new_reservation = borrow_form.save(commit=False)
                new_reservation.tool = tool
                new_reservation.borrower = user

                now = timezone.now()
                if new_reservation.start_date < now:
                    new_reservation.start_date = now

                if tool.shed is not None:
                    new_reservation.lender = tool.shed.coordinator
                    new_reservation.status = 'A'
                else:
                    new_reservation.lender = tool.owner
                    new_reservation.status = 'P'
                new_reservation.save()
                EmailSender.send_borrow_request_email(new_reservation)
                return redirect('/toolshare/list-borrowed-tools/all')
        else:
            # Show the Reservation-form
            borrow_form = BorrowToolForm(requested_tool_id=tool_id)

        # Get all the approved reservations
        now = datetime.datetime.now()
        reservations = Reservation.objects.filter(
            status = 'A',
            tool_id=tool_id,
            end_date__gt=now,
            start_date__lt=now + td(days=90)
        )

        list_disabled_dates = list()
        for reservation in reservations:
            delta = reservation.end_date - reservation.start_date
            for i in range(delta.days + 1):
                disable_date = reservation.start_date + td(days=i)
                list_disabled_dates.append(disable_date.strftime('%m/%d/%Y'))

        return render(request, 'toolshare/borrow-tool.html', {
            'tool': tool,
            'borrow_form': borrow_form,
            'tool_id': tool_id,
            'current_date': datetime.datetime.now().strftime('%m/%d/%Y'),
            'list_disabled_dates': list_disabled_dates
        })

    @staticmethod
    @login_required
    def list_borrowed_tools(request, status):
        if request.method == 'GET':
            user = User.objects.get(pk=request.user.id)
            if status == 'all':
                # Get all the reservations
                reservations = Reservation.objects.filter(
                    borrower_id = user.id,
                ).order_by('-id')
            elif status == 'pending':
                pass
            elif status == 'accepted':
                pass
            elif status == 'return-pending':
                pass
            elif status == 'return-ack':
                pass

            reservation_paginator = Paginator(reservations, ReservationController.PAGE_SIZE_BORROWED_TOOLS)
            page = request.GET.get('page')
            now_date = timezone.now()
            try:
                reservation_page = reservation_paginator.page(page)
            except PageNotAnInteger:
                reservation_page = reservation_paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999),
                # deliver last page of results.
                reservation_page = reservation_paginator.page(reservation_paginator.num_pages)

            return render(request, 'toolshare/list-borrowed-tools.html', {
                'reservation_page': reservation_page,
                'now_date':now_date
            })

    @staticmethod
    @login_required
    def list_tool_arrangements(request, status):
        if request.method == 'GET':
            user = User.objects.get(pk=request.user.id)
            if status == 'all':
                # Get all the reservations
                reservations = Reservation.objects.filter(
                    lender_id = user.id,
                ).order_by('-id')
            elif status == 'pending':
                pass
            elif status == 'accepted':
                pass
            elif status == 'return-pending':
                pass
            elif status == 'return-ack':
                pass

            reservation_paginator = Paginator(reservations, ReservationController.PAGE_SIZE_BORROWED_TOOLS)
            page = request.GET.get('page')
            try:
                reservation_page = reservation_paginator.page(page)
            except PageNotAnInteger:
                reservation_page = reservation_paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999),
                # deliver last page of results.
                reservation_page = reservation_paginator.page(reservation_paginator.num_pages)

            return render(request, 'toolshare/list-tool-arrangements.html', {
                'reservation_page': reservation_page
            })

    @staticmethod
    @login_required
    def cancel_as_borrower(request, reservation_id):
        if request.method == 'GET':
            user = User.objects.get(pk=request.user.id)
            reservation = Reservation.objects.get(pk=reservation_id)
            if request.user.id != reservation.borrower_id:
                messages.add_message(request, messages.WARNING, 'Oops. You are not allowed to change this reservation.')
                return redirect('/toolshare/list-borrowed-tools/all')
            else:
                # Cancel the borrower
                reservation.status = 'C'
                reservation.cancel_msg = 'The borrower cancelled the reservation.'
                reservation.save()
                messages.add_message(request, messages.SUCCESS, 'Your reservation was successfully cancelled.')
                return redirect('/toolshare/list-borrowed-tools/all')

    @staticmethod
    @login_required
    def return_tool(request, reservation_id):
        if request.method == 'GET':
            user = User.objects.get(pk=request.user.id)
            reservation = Reservation.objects.get(pk=reservation_id)
            if request.user.id != reservation.borrower_id:
                messagesadd_message(request, messages.WARNING, 'Oops. You are not allowed to change this reservation.')
                return redirect('/toolshare/list-borrowed-tools/all')
            else:
                now = timezone.now()
                if now < reservation.start_date:
                    messages.add_message(request, messages.WARNING, "Oops. You cannot return a tool that you don't have yet. Try cancelling the reservation.")
                else:
                    reservation.status = 'RP'
                    reservation.tool.status = 'R'
                    reservation.save()
                    reservation.tool.save()
                    messages.add_message(request, messages.SUCCESS, 'You returned the tool.')
                return redirect('/toolshare/list-borrowed-tools/all')

    @staticmethod
    @login_required
    def cancel_as_lender(request, reservation_id):
        if request.method == 'POST':
            user = User.objects.get(pk=request.user.id)
            reservation = Reservation.objects.get(pk=reservation_id)
            cancel_msg = request.POST['lender_message']
            if request.user.id != reservation.lender_id:
                messages.add_message(request, messages.WARNING, 'Oops. You are not allowed to change this reservation.')
            else:
                # Cancel the
                now = timezone.now()
                if reservation.start_date < now and now < reservation.end_date:
                    messages.add_message(request, messages.WARNING, 'The tool is currently being used by the borrower. You cannot cancel it.')
                else:
                    reservation.status = 'C'
                    reservation.cancel_msg = cancel_msg
                    reservation.save()
                    messages.add_message(request, messages.SUCCESS, 'The reservation was successfully cancelled.')
                    EmailSender.send_cancel_request_email(reservation)
            return redirect('/toolshare/list-tool-arrangements/all')

    @staticmethod
    @login_required
    def respond_reservation(request, reservation_id):
        if request.method == 'POST':
            #user = User.objects.get(pk=request.user.id)
            reservation = Reservation.objects.get(pk=reservation_id)
            if request.user.id != reservation.lender_id:
                messages.add_message(request, messages.WARNING, 'Oops. You are not allowed to change this reservation.')
            else:
                now = timezone.now()
                if reservation.end_date < now:
                    # Cancel automatically
                    reservation.status = 'C'
                    reservation.cancel_msg = 'Reservation was auto cancelled. The reservation date already passed'
                    messages.add_message(request, messages.ERROR, reservation.cancel_msg)
                elif 'button_approve' in request.POST:
                    # Approve
                    reservation.status = 'A'
                    reservation.tool.status = 'B'
                    messages.add_message(request, messages.SUCCESS, 'The reservation was Approved.')
                elif 'button_reject' in request.POST:
                    # Reject
                    reservation.status = 'R'
                    reject_msg = request.POST['lender_message']
                    reservation.reject_msg = reject_msg
                    messages.add_message(request, messages.SUCCESS, 'The reservation was Rejected.')
                reservation.save()
                reservation.tool.save()
                EmailSender.send_approve_reject_request_email(reservation)
            return redirect('/toolshare/list-tool-arrangements/all')

    @staticmethod
    @login_required
    def acknowledge_return_tool(request, reservation_id):
        if request.method == 'POST':
            user = User.objects.get(pk=request.user.id)
            reservation = Reservation.objects.get(pk=reservation_id)
            if request.user.id != reservation.lender_id:
                messages.add_message(request, messages.WARNING, 'Oops. You are not allowed to change this reservation.')
            else:
                if 'button_reject' in request.POST:
                    reservation.status = 'RD'
                    reservation.tool.status = 'L'
                    reservation.save()
                    reservation.tool.save()
                    messages.add_message(request, messages.SUCCESS, 'You just confirmed that the tool was LOST.')

                elif 'button_confirm' in request.POST:

                    reservation.status = 'RA'
                    reservation.tool.status = 'A'
                    reservation.save()
                    reservation.tool.save()
                    messages.add_message(request, messages.SUCCESS, 'You just confirmed that the tool was returned.')
            return redirect('/toolshare/list-tool-arrangements/all')

    @staticmethod
    @login_required
    def generate_statistics(request):
            reserves = Reservation.objects.all()
            tools = Tool.objects.all()

            pending_reserves = [(c, c.id, reserves.filter(lender=c.id, status='P').count()) for c in Tool.objects.all()]
            pending_reserves.sort(key = lambda x:x[2], reverse=True)
            pending_reserves = pending_reserves[0:5]

            owned_tools = [(c, c.id, tools.filter(owner=c.id,).count()) for c in User.objects.all()]
            owned_tools.sort(key = lambda x:x[2], reverse=True)
            owned_tools = owned_tools[0:5]

            #Dead code that implements new community statistics
            """
            top_zones = [(c, c.id, tools.filter(owner=c.id,).count()) for c in Sharezone.objects.all()]
            top_zones.sort(key = lambda x:x[2], reverse=True)
            top_zones = top_zones[0:5]

            popular_users = [(c, c.id, tools.filter(owner=c.id,).count()) for c in User.objects.all()]
            popular_users.sort(key = lambda x:x[2], reverse=True)
            popular_users = popular_users[0:5]
            """

            return render(request, 'toolshare/statistics.html', {
                'top_sharers'   :   owned_tools,
                'top_tools'     :   pending_reserves
            })

            """,
                'top_zones'     :   top_zones,
                'popular_users' :   popular_users
            """