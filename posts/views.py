from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Post
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required #login required para las urls que solo son de usuario registrado
from django.utils.decorators import method_decorator
from .forms import PostCreateForm
from django.http import HttpResponseRedirect

from django.views.generic.detail import DetailView


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
    

@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
    template_name = "posts/post_detail.html"
    model = Post
    context_object_name = 'post'



@login_required
def like_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        messages.add_message(request, messages.INFO, "Ya no te gusta esta publicacion")
        post.likes.remove(request.user)
    else:
        messages.add_message(request, messages.INFO, "Te gusta esta publicacion")
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[pk]))