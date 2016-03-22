from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from toolshare.models.shed import Shed
from toolshare.models.user import User
from toolshare.views.base_controller import BaseController
from toolshare.forms.forms_shed import ShedForm


# Create your views here.
class ShedController(BaseController):
    PAGE_SIZE = 10

    @staticmethod
    @login_required
    def create_shed(request):
        if request.method == 'POST':
            shedcreation_form = ShedForm(request.POST)
            if shedcreation_form.is_valid():
                # Generate the new-shed from the Form
                new_shed = shedcreation_form.save(commit=False)
                user = User.objects.get(pk=request.user.id)
                new_shed.coordinator=user
                new_shed.save()
                return redirect('/toolshare/list-sheds')
        else:
            shedcreation_form = ShedForm()

        return render(request, 'toolshare/create-shed.html',{
        'shedcreation_form': shedcreation_form
        })

    @staticmethod
    @login_required
    def list_sheds(request):
        if request.method == 'GET':
            user = User.objects.get(pk=request.user.id)
            user_sheds = user.shed_set.all()
            shed_paginator = Paginator(user_sheds, ShedController.PAGE_SIZE)

            page = request.GET.get('page')
            try:
                shed_page = shed_paginator.page(page)
            except PageNotAnInteger:
                shed_page = shed_paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999),
                # deliver last page of results.
                shed_page = shed_paginator.page(shed_paginator.num_pages)

            return render(request, 'toolshare/list-sheds.html',{
            'shed_page': shed_page,
            'user_sheds': user_sheds
            })
