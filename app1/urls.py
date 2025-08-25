from django.contrib import admin
from django.urls import include, path
from . import views
from . import api
from django.contrib.auth.views import PasswordChangeDoneView,PasswordResetDoneView,PasswordResetView,PasswordResetConfirmView,PasswordResetCompleteView
from . import api_view
from rest_framework import routers
router=routers.DefaultRouter()
router.register('student-test', api_view.StudentViewSet, basename='student-test')

urlpatterns = [
    path("",include(router.urls)),
    path("accounts/login/",views.login_page, name="login_page"),
    path("accounts/logout/",views.logout_page, name="logout_page"),
	path('',views.index,name='home'),
    path('about/',views.about,name='about'),
    path('student/',views.student,name='student'),
    path('student-data/<int:id>/', views.single_student,name='single_student'),
    path('student-delete/<int:id>/', api.delete_student,name='delete_student'),
    path('filter-student/',views.filter_students,name='filter_student'),
    path('filter-student-api/',api.filter_students_api,name='filter_student_api'),
    
    
    
    path('password-reset/',PasswordResetView.as_view(),name="password_reset"),
    path('password-reset/done/',PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    
    
    
    # api student
    path('student-api/',api_view.student_list,name='student-api')
]
