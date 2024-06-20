from django.urls import path
from .import views


urlpatterns=[
      path('',views.home,name='home'),
      path('admin_login',views.admin_login,name='admin_login'),
      path('user_login',views.user_login,name='user_login'),
      path('admin_home',views.admin_home,name='admin_home'),
      path('user_home',views.user_home,name='user_home'),
      path('create_user',views.create_user,name='create_user'),
      path('user_logout',views.user_logout,name='user_logout'),
      path('add_lead',views.add_lead,name='add_lead'),
      path('edit_lead/<int:i>',views.edit_lead,name='edit_lead'),
      path('save_edited',views.save_edited,name='save_edited'),
      path('user_report/<int:i>',views.user_report,name='user_report'),
      path('ajax/check-username/', views.check_username, name='check_username'),
      path('change_password',views.change_password,name="change_password"),
      path('suspend_user/<int:i>',views.suspend_user,name='suspend_user'),
      path('activate_user/<int:i>',views.activate_user,name='activate_user'),
      path('users_page',views.users_page,name='users_page'),
      path('course_wise_report',views.course_wise_report,name='course_wise_report'),
      path('lead_profile/<int:i>',views.lead_profile,name='lead_profile'),
      path('ajax/check_phone_number/', views.check_phone_number, name='check_phone_number'),
      path('check_phone_number2', views.check_phone_number2,name='check_phone_number2'),
      path('check_phone_number3', views.check_phone_number3,name='check_phone_number3'),
      path('check_phone_number4', views.check_phone_number4,name='check_phone_number4'),
      path('saved_lead_profile',views.saved_lead_profile,name='saved_lead_profile'),
      path('edited_lead_profile',views.edited_lead_profile,name='edited_lead_profile'),
      path('delete_lead/<int:lead_id>/', views.delete_lead, name='delete_lead'),
      path('search_with_phone',views.search_with_phone,name='search_with_phone'),
      path('notifications',views.notifications_page,name='notifications'),
      path('mark_read/<int:i>',views.mark_read,name='mark_read'),
      path('view_notification_profile/<int:i>',views.view_notification_profile,name='view_notification_profile'),
      path('edit_from_profile',views.edit_from_profile,name='edit_from_profile')
]
