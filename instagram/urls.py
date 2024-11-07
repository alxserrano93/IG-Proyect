from django.contrib import admin
from django.urls import path

from .views import HomeView, LoginView, RegisterView, LegalView, ContactView, logout_view

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name = 'register'),
    path('contact/', ContactView.as_view(), name = 'contact'),
    path('legal/', LegalView.as_view(), name = 'legal'),


    path('admin/', admin.site.urls),

]
