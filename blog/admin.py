from django.contrib import admin
from parler.admin import TranslatableAdmin
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import (
    Post, Category, Tag, Experience, Project, About,
    ContactMessage, DownloadedMedia
)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': CKEditorWidget(),
        }


class PostAdmin(TranslatableAdmin):
    form = PostForm
    list_display = ('title', 'author', 'category', 'is_published', 'is_featured', 'views', 'published_at')
    list_filter = ('is_published', 'is_featured', 'category', 'created_at')
    search_fields = ('translations__title', 'translations__content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views', 'created_at', 'updated_at')
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'author')
        }),
        ('Organization', {
            'fields': ('category', 'tags')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class CategoryAdmin(TranslatableAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('translations__name',)
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(TranslatableAdmin):
    list_display = ('name', 'slug', 'color')
    search_fields = ('translations__name',)
    prepopulated_fields = {'slug': ('name',)}


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'
        widgets = {
            'description': CKEditorWidget(),
            'achievements': CKEditorWidget(),
        }


class ExperienceAdmin(TranslatableAdmin):
    form = ExperienceForm
    list_display = ('position', 'company', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current', 'start_date')
    search_fields = ('company', 'position', 'translations__description')
    readonly_fields = ('created_at',)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'description': CKEditorWidget(),
        }


class ProjectAdmin(TranslatableAdmin):
    form = ProjectForm
    list_display = ('title', 'is_featured', 'created_at', 'updated_at')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('translations__title', 'translations__technologies')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = '__all__'
        widgets = {
            'bio': CKEditorWidget(),
        }


class AboutAdmin(TranslatableAdmin):
    form = AboutForm
    list_display = ('title', 'email', 'location', 'cv_auto_update')
    search_fields = ('translations__title', 'email')
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('Profile', {
            'fields': ('title', 'bio', 'profile_image', 'email', 'phone', 'location')
        }),
        ('Skills & CV', {
            'fields': ('skills', 'resume_file', 'cv_auto_update')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('System', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Message Info', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )


class DownloadedMediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'file_size', 'downloaded_at')
    list_filter = ('media_type', 'downloaded_at')
    search_fields = ('title', 'original_url')
    readonly_fields = ('file_size', 'downloaded_at', 'original_url')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(DownloadedMedia, DownloadedMediaAdmin)
