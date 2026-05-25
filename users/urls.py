
from users import views
from django.urls import path

from django.contrib.auth import views as auth_views
from django.urls import path
urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("payment/",views.create_order,name="payment"),
    # enter email
    path("password-reset/",auth_views.PasswordResetView.as_view(),name="password_reset"),
    # email sent page
    path("password-reset/done/",auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    #user clicks email link 
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    # password changed successfully
    path("reset/done/",auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    
]

