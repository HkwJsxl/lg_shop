from django.urls import path, re_path
from . import views

urlpatterns = [
    path("check/<str:username>/", views.CheckUserView.as_view()),
    path("mobile/<str:mobile>/", views.CheckMobileView.as_view()),
    re_path(r"^code/(?P<uuid>[\w-]+)/$", views.VerifyCodeView.as_view()),
]
