from django.urls import path
from formcontact.views import ContactView



urlpatterns = [
    path('',ContactView.as_view()),
]