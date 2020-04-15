from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.LoginSessionView.as_view(template_name='registration/login.html')),
]