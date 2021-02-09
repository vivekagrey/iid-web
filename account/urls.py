from . import views
from django.urls import path

app_name = 'account'

urlpatterns = [
    path('profile/', views.profile_view, name="profile"),
    path('mycourses/', views.MyCourses, name='mycourses'),
    path('lesson_list/<slug>/', views.LessonList, name="lesson_list"),
    path('training-schedule/', views.schedule, name="schedule"),
    path('activate/<uidb64>/<token>', views.activate,
         name='activate'),
]
