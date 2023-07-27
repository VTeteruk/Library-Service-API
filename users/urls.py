from django.urls import path

from users.views import UserView

urlpatterns = [
    path("me/", UserView.as_view(), name="me")
]

app_name = "users"
