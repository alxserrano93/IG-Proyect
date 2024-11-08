from django.contrib import admin
from django.urls import path

from .views import HomeView, LoginView, RegisterView, ContactView, LegalView, logout_view, ProfileDetailView, ProfileUpdateView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name = 'register'),
    path('contact/', ContactView.as_view(), name = 'contact'),
    path('profile/<pk>/', ProfileDetailView.as_view(), name = 'profile_detail'),
    path('profile/update/<pk>/', ProfileUpdateView.as_view(), name='profile_update'),
    path('legal/', LegalView.as_view(), name = 'legal'),


    path('admin/', admin.site.urls),

]
