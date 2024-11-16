from django. shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect

from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.views import View

from django.contrib.auth.decorators import login_required #login required para las urls que solo son de usuario registrado
from django.utils.decorators import method_decorator

from django.urls import reverse_lazy, reverse
from .forms import RegistrationForm, LoginForm, ProfileFollow
from profiles.models import UserProfile, Follow
from profiles.forms import FollowForm
from posts.models import Post


class HomeView(TemplateView):
    template_name = "general/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Si el usuario está logueado
        if self.request.user.is_authenticated:
            # Obtenemos los posts de los usuarios que seguimos
            seguidos = Follow.objects.filter(follower=self.request.user.profile).values_list('following__user', flat=True)
            # Nos traemos los posts de los usuarios que seguimos
            last_posts = Post.objects.filter(user__profile__user__in=seguidos)

        else:
            last_posts = Post.objects.all().order_by('-created_at')[:10]
        context['last_posts'] = last_posts

        return context

        

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



# @method_decorator(login_required, name='dispatch')
# class ProfileDetailView(DetailView):
#     model = UserProfile
#     template_name = "general/profile_detail.html"
#     context_object_name = 'profile'



# @method_decorator(login_required, name='dispatch')
# class FollowProfileView(View):
#     def post(self, request, *args, **kwargs):
#         profile_id = request.POST.get('profile_pk')
#         profile_to_follow = get_object_or_404(UserProfile, pk=profile_id)
        
#         # Lógica para seguir al perfil
#         request.user.profile.follow(profile_to_follow)
        
#         # Mensaje de éxito
#         messages.success(request, f'Has comenzado a seguir a {profile_to_follow.user.username}')
        
#         # Redirige al perfil del usuario seguido o al perfil actual
#         return redirect(reverse('profile_detail', args=[profile_id]))

@method_decorator(login_required, name="dispatch")
class ProfileDetailView(DetailView, FormView):
    model = UserProfile
    template_name = "general/profile_detail.html"
    context_object_name = "profile"
    form_class = FollowForm

    def get_initial(self):
        self.initial['profile_pk'] = self.get_object().pk
        return super().get_initial()
    
    def form_valid(self, form):
        profile_pk = form.cleaned_data.get('profile_pk')
        action = form.cleaned_data.get('action')
        following = UserProfile.objects.get(pk=profile_pk)

        if Follow.objects.filter(
            follower=self.request.user.profile,
            following = following
        ).count():
            Follow.objects.filter(
                follower = self.request.user.profile,
                following = following
            ).delete()
            messages.add_message(self.request, messages.SUCCESS, f'Se ha dejado de seguir a {following.user.username}')

        else:
            Follow.objects.get_or_create(
                follower = self.request.user.profile,
                following = following
            )
            messages.add_message(self.request, messages.SUCCESS, f'Acabas de seguir a {following.user.username}')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('profile_detail', args=[self.get_object().pk])
    
    def context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Comprobamos si seguimos al usuario
        following = Follow.objects.filter(follower=self.request.user.profile, following = self.get_object()).exists()
        context['following'] = following
        return context



@method_decorator(login_required, name='dispatch')
class ProfileListView(ListView):
    model = UserProfile
    template_name = "general/profile_list.html"
    context_object_name = 'profiles' 

    def get_queryset(self):
        return UserProfile.objects.all().exclude(user=self.request.user)



@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = "general/profile_update.html"
    context_object_name = "profile"
    fields = ['profile_picture', 'bio', 'birth_date']

    #Seguridad para que solo vayan a esta url si estan en el perfil creado
    def dispatch(self, request, *args, **kwargs):
        user_profile = self.get_object()
        if user_profile.user != self.request.user:
            return HttpResponseRedirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Perfil editado correctamente.")
        return super(ProfileUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('profile_detail', args=[self.request.object.pk])



@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Se ha cerrado sesión correctamente.")
    return HttpResponseRedirect(reverse('home'))