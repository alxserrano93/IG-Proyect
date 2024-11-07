from django. shortcuts import render

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib import messages

from django.urls import reverse_lazy
from .forms import RegistrationForm


class HomeView(TemplateView):
    template_name = "general/home.html"


class LoginView(TemplateView):
    template_name = "general/login.html"


class RegisterView(CreateView):
    template_name = "general/register.html"
    model = User
    success_url = reverse_lazy('home')
    form_class = RegistrationForm

    def form_valid(self, form):
        # `form_valid` es un método que se ejecuta cuando el formulario es válido (cuando pasa todas las validaciones)
        response = super().form_valid(form) # Llama al método `form_valid` original para procesar el formulario y guardar el nuevo usuario
        messages.add_message(self.request, messages.SUCCESS, "Usuario creadoo correctamente") # Agrega un mensaje de éxito a la solicitud
        return response # Retorna la respuesta para que se ejecute la redirección


class LegalView(TemplateView):
    template_name = "general/legal.html"


class ContactView(TemplateView):
    template_name = "general/contact.html"