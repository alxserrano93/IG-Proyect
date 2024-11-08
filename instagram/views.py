from django. shortcuts import render, HttpResponseRedirect

from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from django.urls import reverse_lazy, reverse
from .forms import RegistrationForm, LoginForm
from profiles.models import UserProfile


class HomeView(TemplateView):
    template_name = "general/home.html"



class LoginView(FormView):
    template_name = "general/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=usuario, password=password)

        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f'Bienvenido de nuevo {user.username}')
            return HttpResponseRedirect(reverse('home'))

        else:
            messages.add_message(
                self.request, messages.ERROR, 'Usuario no valido o contraseña no valida')
            return super(LoginView, self).form_invalid(form)
    


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



class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = "general/profile_detail.html"
    context_object_name = 'profile' 



class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = "general/profile_update.html"
    context_object_name = "profile"
    fields = ['profile_picture', 'bio', 'birth_date']
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Perfil editado correctamente.")
        return super(ProfileUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('profile_detail', args=[self.object.pk])



def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Se ha cerrado sesión correctamente.")
    return HttpResponseRedirect(reverse('home'))