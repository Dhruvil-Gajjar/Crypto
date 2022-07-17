from django.urls import path
from django.contrib.auth import views as auth_views

from users.views import *


urlpatterns = [
    # Authentication
    path('signup/', user_signup, name='user_signup'),
    path('activate/<uuid:uid>/<str:token>/', activate_user, name='activate_user'),
    path('resend-activation-email/', resend_activation_email, name='resend_activation_email'),

    path('login/', UserLoginView.as_view(template_name = 'Auth/login-new.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/change-password/', auth_views.PasswordChangeView.as_view(template_name='Auth/change_password.html'),
         name='change_password'),
    path('profile/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='Auth/success.html'),
         name='password_change_done'),

    path("password_reset/", password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Auth/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="Auth/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='Auth/password_reset_complete.html'),
         name='password_reset_complete'),

    # List
    path('users/list/', list_users, name='list_users'),

    # Add/Edit
    path('manage/user/', manage_user, name='add_user'),
    path('manage/user/<uuid:uid>/', manage_user, name='edit_user'),

    # Update My Profile
    path('view/user-profile/', view_profile, name='view_profile'),
    path('update/user/<uuid:uid>/', update_profile, name='update_profile'),

    # Delete/Action
    path('users/action/<str:action>/<uuid:uid>/', user_action, name='user_action'),
]
