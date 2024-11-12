from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Post
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required #login required para las urls que solo son de usuario registrado
from django.utils.decorators import method_decorator

from .forms import PostCreateForm


# Create your views here.
@method_decorator(login_required, name='dispatch') #Da seguridad de que un usuario sin login no puede ir a esta urls 
class PostCreateView(CreateView):
    template_name = "posts/post_create.html"
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, "Publicacion creada correctamente")
        return super(PostCreateView, self).form_valid(form)
    