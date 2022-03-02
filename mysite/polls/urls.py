from django.urls import path
from .views import * 

urlpatterns = [
    path("",IndexView.as_view(),name="home"),
    path("<int:pk>/",DetailsView.as_view(),name="details"),
    path("<int:pk>/results",ResultsView.as_view(),name="results"),
    path("<int:question_id>/vote",vote,name="vote"),
    path("login-user/",loginFunction,name="login"),
    path("register/",register,name="register"),
    path("account_activation_sent/",account_activation_sent, name="account_activation_sent"),
    path("activate/<str:uidb64>/<str:token>/",activate, name="activate")
]
