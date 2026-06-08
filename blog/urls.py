from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('experience/', views.ExperienceListView.as_view(), name='experience-list'),
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('resume/', views.ResumeDownloadView.as_view(), name='resume-download'),
    path('search/', views.SearchView.as_view(), name='search'),
]
