from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from .models import Post, Category, Tag, Experience, Project, About, ContactMessage
from .forms import ContactForm
from .utils import generate_pdf_resume


class IndexView(TemplateView):
    """Homepage view"""
    template_name = 'blog/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = Post.objects.filter(
            is_published=True,
            is_featured=True
        )[:3]
        context['featured_projects'] = Project.objects.filter(
            is_featured=True
        )[:3]
        context['recent_posts'] = Post.objects.filter(
            is_published=True
        )[:5]
        return context


class PostListView(ListView):
    """Blog posts list view"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True)
        category_slug = self.request.GET.get('category')
        tag_slug = self.request.GET.get('tag')
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        
        return queryset.order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['tags'] = Tag.objects.all()
        return context


class PostDetailView(DetailView):
    """Blog post detail view"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        post = self.get_object()
        post.views += 1
        post.save()
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['related_posts'] = Post.objects.filter(
            is_published=True,
            category=post.category
        ).exclude(id=post.id)[:3]
        return context


class AboutView(TemplateView):
    """About page view"""
    template_name = 'blog/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = About.objects.first()
        context['experiences'] = Experience.objects.all().order_by('-start_date')
        return context


class ExperienceListView(ListView):
    """Experience/Career timeline view"""
    model = Experience
    template_name = 'blog/experience_list.html'
    context_object_name = 'experiences'
    
    def get_queryset(self):
        return Experience.objects.all().order_by('-start_date')


class ProjectListView(ListView):
    """Projects portfolio view"""
    model = Project
    template_name = 'blog/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        return Project.objects.all().order_by('-created_at')


class ProjectDetailView(DetailView):
    """Project detail view"""
    model = Project
    template_name = 'blog/project_detail.html'
    context_object_name = 'project'
    slug_field = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['related_projects'] = Project.objects.exclude(
            id=project.id
        ).order_by('-created_at')[:3]
        return context


class ContactView(FormView):
    """Contact form view"""
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('blog:contact')
    
    def form_valid(self, form):
        ContactMessage.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            subject=form.cleaned_data['subject'],
            message=form.cleaned_data['message'],
        )
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = About.objects.first()
        return context


class ResumeDownloadView(TemplateView):
    """Download CV/Resume as PDF"""
    
    def get(self, request, *args, **kwargs):
        about = About.objects.first()
        if not about:
            return HttpResponse("About page not configured", status=400)
        
        experiences = Experience.objects.all().order_by('-start_date')
        projects = Project.objects.filter(is_featured=True)[:5]
        
        pdf = generate_pdf_resume(about, experiences, projects, request.LANGUAGE_CODE)
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="resume_{request.LANGUAGE_CODE}.pdf"'
        return response


class SearchView(ListView):
    """Search posts and projects"""
    template_name = 'blog/search.html'
    context_object_name = 'results'
    paginate_by = 20
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if not query:
            return []
        
        posts = Post.objects.filter(
            Q(translations__title__icontains=query) |
            Q(translations__content__icontains=query),
            is_published=True
        )
        
        projects = Project.objects.filter(
            Q(translations__title__icontains=query) |
            Q(translations__description__icontains=query)
        )
        
        return list(posts) + list(projects)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

