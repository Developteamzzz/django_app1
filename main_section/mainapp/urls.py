from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.main,name='main'),
    path('main',views.main,name='main'),
    path('first',views.first,name='first'),
    path('signup',views.signup,name='signup'),
    path('loginmain',views.loginmain,name='loginmain'),
    path('signupcomplete/', views.signupcomplete, name='signupcomplete'),
    path('course_detail/<int:studentid>/<int:courseid>/', views.course_detail, name='course_detail'),
    path('otp_verify',views.otp_verify,name='otp_verify'),
    #path('my_view',views.my_view,name='my_view'),
    #path('resend_otp',views.resend_otp,name='resend_otp'),
    path('success_msg',views.success_msg,name='success_msg'),
    path('course_pro/<int:courseid>/<int:studentid>/',views.course_pro,name='course_pro'),
    path('validate_username',views.validate_username, name='validate_username'),
    path('ajax/message/', views.ajax_message, name='ajax_message'),
    path('signout',views.signout,name='signout'),
    path('contact',views.contact,name='contact'),
    path('check_profile_status/<int:student_id>/',views.check_profile_status, name='check_profile_status'),
    path('maincourse',views.maincourse,name='maincourse'),
    # path('change_applied/<int:studentid>/<int:courseid>/',views.change_applied,name='change_applied'),
    path('user_pro', views.user_pro, name='user_pro'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


