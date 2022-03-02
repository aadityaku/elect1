
from django.contrib import admin
from django.urls import path ,include
from polls.views import *
urlpatterns = [
    path('', include("polls.urls")),
    path('admin/', admin.site.urls),
]
