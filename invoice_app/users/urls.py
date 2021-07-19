from django.urls import path

from invoice_app.users.views import (
    UserRedirectView,
    UserUpdateView,
    UserDetailView,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", UserRedirectView.as_view(), name="redirect"),
    path("~update/", UserUpdateView.as_view(), name="update"),
    path("<str:username>/", UserDetailView.as_view(), name="detail"),
]
