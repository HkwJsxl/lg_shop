from django.urls import path, re_path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("check/<str:username>/", views.CheckUserView.as_view()),
    path("mobile/<str:mobile>/", views.CheckMobileView.as_view()),
]
