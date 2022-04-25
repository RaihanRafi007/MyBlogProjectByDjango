from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from django.shortcuts import render,HttpResponseRedirect, redirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, View, TemplateView, DeleteView
from App_Blog.models import Blog, Comment, Likes
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
from App_Blog.forms import CommentForm
from django.template.defaultfilters import slugify, title
from .utils import slugify_instance_title

# Create your views here.
"""
def search_view(request):
    query = request.GET.get('q')
    qs = Blog.objects.search(query=query)
    context = {
        "object_list": qs
    }
    return render(request, "App_Blog/search.html", context=context)
"""
class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = 'App_Blog/my_blogs.html'

def blog_list(request):
    return render(request, 'App_Blog/blog_list.html', context={})
    

class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    template_name= 'App_Blog/create_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image',)
    
    def form_valid(self, form):
       blog_obj = form.save(commit = False) #commit = True
       blog_obj.author = self.request.user
       #title = blog_obj.blog_title
       
       #blog_obj.slug = slugify_instance_title(instance,title, save=True)
       #blog_obj.slug= title.replace(" ", "-") + "-" + str(uuid.uuid4())
       blog_obj.save()
       #return redirect(blog_obj.get_absolute_url())
       return HttpResponseRedirect(reverse('index'))

class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'App_Blog/blog_list.html'

@login_required
def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
  
    comment_form = CommentForm()
    already_liked = Likes.objects.filter(blog=blog, user=request.user)
    if already_liked:
        liked = True
    else:
        liked = False
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug':slug}))

    return render(request, 'App_Blog/blog_details.html', context={'blog':blog, 'comment_form':comment_form, 'liked':liked})


@login_required
def liked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    if not already_liked:
        liked_post = Likes(blog=blog, user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug':blog.slug}))


@login_required
def unliked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug':blog.slug}))

class UpdateBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = {'blog_title', 'blog_content', 'blog_image'}
    template_name = 'App_Blog/edit_blog.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('App_Blog:blog_details', kwargs={'slug':self.object.slug})

@login_required
def delete(request, pk):
    blog = Blog.objects.get(pk=pk)
    blog.delete()
    return HttpResponseRedirect(reverse('App_Blog:my_blogs'))
   