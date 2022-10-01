from django.urls import path
from . import views
urlpatterns = [
    path('registration/', views.HirerRegistration.as_view()),
    path('login/', views.HirerLogin.as_view()),
    path('logout/', views.HirerLogout.as_view()),
    path('profile/', views.HirerProfile.as_view()),
    path('opportunity/', views.HiringList.as_view()),
]