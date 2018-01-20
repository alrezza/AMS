from django.conf.urls import url
from . import views

app_name = 'ams'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^subordinates/$', views.subordinates, name='subordinates'),
    url(r'^subordinates/(?P<employee_id>[0-9]+)/approval/$', views.approval, name='approval'),
    url(r'^subordinates/(?P<ownership_id>[0-9]+)/approved/$', views.approved, name='approved'),
    url(r'^employees/$', views.employees, name='employees'),
    url(r'^employees/(?P<employee_id>[0-9]+)/$', views.employee_detail, name='employee_detail'),
    url(r'^employee_report/$', views.employee_report, name='employee_report'),
    url(r'^asset_report/$', views.asset_report, name='asset_report'),
    url(r'^request_asset/$', views.request_asset, name='request_asset'),
]
