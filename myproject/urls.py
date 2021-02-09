from django.contrib import admin
from django.urls import path, include
from account.views import login_view, logout_view
from django.contrib.auth import views as auth_views  # for pass change and reset views
from django.conf import settings  # for profile pic
from django.conf.urls.static import static  # for profile pic

from django.views.defaults import page_not_found, permission_denied, bad_request, server_error
from django.http import Http404
from django.views.generic.base import RedirectView
from django.views.csrf import csrf_failure

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls', namespace='app')),
    path('account/', include('account.urls', namespace='account')),
    # path('', include('django.contrib.auth.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('captcha/', include('captcha.urls')),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)

    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(html_email_template_name='registration/password_reset_email.html'), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('404/', page_not_found, {'exception': Http404()}),
    path('403/', permission_denied, {'exception': Http404()}),
    path('500/', server_error),
    path('400/', bad_request, {'exception': Http404()}),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

