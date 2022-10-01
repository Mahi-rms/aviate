
from django.urls import path
from . import views
urlpatterns = [
    path('registration/', views.Registration.as_view()),
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
    path('profile/', views.UserProfile.as_view()),
    path('opportunities/', views.OpportunityList.as_view()),
    path('opportunities/<uuid:opportunity_id>', views.Application.as_view()),
    path('applications/', views.Applied.as_view()),
    path('applications/withdraw/<uuid:application_id>', views.WithdrawApplication.as_view()),
    path('applications/archived', views.ArchivedApplications.as_view()),
]