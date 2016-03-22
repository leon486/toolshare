from django.conf.urls import patterns, url
from toolshare.views.base_controller import BaseController
from toolshare.views.user_controller import UserController
from toolshare.views.tool_controller import ToolController
from toolshare.views.shed_controller import ShedController
from toolshare.views.reservation_controller import ReservationController
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='toolshare/index.html'), name='index'),
    url(r'^user-registration$', UserController.register_user, name='user-registration'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'toolshare/login.html'} ,name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout',{'next_page': '/toolshare'}, name='logout'),
    url(r'^my_account$', UserController.my_account, name='my_account'),
    url(r'^change-personal-info$', UserController.change_personal_info, name='change-personal-info'),
    url(r'^create-shed$', ShedController.create_shed, name='create-shed'),
    url(r'^list-sheds$', ShedController.list_sheds, name='list-sheds'),
    url(r'^find_tool$', ToolController.find_tool, name='find_tool'),

    url(r'^change-preferences$', UserController.change_user_preferences, name='change-preferences'),
    url(r'^tool-registration$', ToolController.register_tool, name='tool-registration'),
    url(r'^list-owned-tools$', ToolController.list_owned_tools, name='list-owned-tools'),
    url(r'^borrow-tool/(\d+)$', ReservationController.borrow_tool, name='borrow-tool'),
    url(r'^tool-detail/(\d+)$', ToolController.tool_detail, name='tool-detail'),
    url(r'^change-tool-info/(\d+)$', ToolController.change_tool_info, name='change-tool-info'),
    url(r'^list-borrowed-tools/(?P<status>\w+)$', ReservationController.list_borrowed_tools, name='list-borrowed-tools'),
    url(r'^list-tool-arrangements/(?P<status>\w+)$', ReservationController.list_tool_arrangements, name='list-user-tools'),
    url(r'^testing$', TemplateView.as_view(template_name='toolshare/testing.html'), name='testing'),
    url(r'^change-tool-availability/(\d+)$', ToolController.change_availability_tool, name='change-tool-availability'),
    url(r'^reservation/(\d+)/cancel-as-borrower$', ReservationController.cancel_as_borrower, name='cancel-as-borrower'),
    url(r'^reservation/(\d+)/return-tool$', ReservationController.return_tool, name='return-tool'),
    url(r'^reservation/(\d+)/cancel-as-lender$', ReservationController.cancel_as_lender, name='cancel-as-lender'),
    url(r'^reservation/(\d+)/respond_reservation', ReservationController.respond_reservation, name='respond_reservation'),
    url(r'^reservation/(\d+)/ack-return-tool$', ReservationController.acknowledge_return_tool, name='ack-return-tool'),
    url(r'^statistics$', ReservationController.generate_statistics, name='statistics'),
    url(r'^activate-deactivate/(\d+)$', ToolController.activate_deactivate_tool, name='activate-deactivate'),


    # Deprecated URLs:
    # ----------------
    #url(r'^index$', TemplateView.as_view(template_name='toolshare/index.html'), name='index'),
    #url(r'^login$', UserController.login_user, name='login'),
    #url(r'^user-home', TemplateView.as_view(template_name='toolshare/user-home.html'), name='user-home'),
)
