from django.db import models
from django.utils.text import slugify
from django.contrib.sitemaps import Sitemap
from ckeditor.fields import RichTextField
from parler.models import TranslatableModel, TranslatedFields
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class SEOMixin(models.Model):
    """Mixin for SEO fields"""
    meta_title = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("SEO title for search engines")
    )
    meta_description = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("SEO description for search engines")
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("SEO keywords (comma-separated)")
    )
    
    class Meta:
        abstract = True


class Category(TranslatableModel):
    """Blog post category with multi-language support"""
    slug = models.SlugField(unique=True, max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
        description=models.TextField(blank=True)
    )
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(TranslatableModel):
    """Blog post tags"""
    slug = models.SlugField(unique=True, max_length=100)
    color = models.CharField(max_length=7, default="#6366f1")
    created_at = models.DateTimeField(auto_now_add=True)
    
    translations = TranslatedFields(
        name=models.CharField(max_length=100)
    )
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(TranslatableModel, SEOMixin):
    """Blog post with multi-language and rich text support"""
    slug = models.SlugField(unique=True, max_length=200)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    featured_image = models.ImageField(
        upload_to='blog/featured/',
        blank=True,
        null=True
    )
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    translations = TranslatedFields(
        title=models.CharField(max_length=200),
        content=RichTextField(),
        excerpt=models.TextField(blank=True, max_length=500)
    )
    
    class Meta:
        ordering = ['-published_at']
        verbose_name_plural = "Posts"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.slug})


class Experience(TranslatableModel, SEOMixin):
    """Work/Professional Experience"""
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    company_logo = models.ImageField(
        upload_to='experience/',
        blank=True,
        null=True
    )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    translations = TranslatedFields(
        description=RichTextField(),
        achievements=RichTextField(blank=True),
    )
    
    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = "Experiences"
    
    def __str__(self):
        return f"{self.position} at {self.company}"


class Project(TranslatableModel, SEOMixin):
    """Portfolio Project"""
    slug = models.SlugField(unique=True, max_length=200)
    featured_image = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True
    )
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    translations = TranslatedFields(
        title=models.CharField(max_length=200),
        description=RichTextField(),
        technologies=models.CharField(max_length=500),
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Projects"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class About(TranslatableModel, SEOMixin):
    """About page content"""
    slug = models.SlugField(unique=True, default='about')
    profile_image = models.ImageField(
        upload_to='about/',
        blank=True,
        null=True
    )
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    resume_file = models.FileField(upload_to='resume/', blank=True, null=True)
    cv_auto_update = models.BooleanField(
        default=True,
        help_text=_("Auto-generate CV from blog data")
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    translations = TranslatedFields(
        title=models.CharField(max_length=200),
        bio=RichTextField(),
        skills=models.TextField(),
    )
    
    class Meta:
        verbose_name_plural = "About"
    
    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class DownloadedMedia(models.Model):
    """Store downloaded media from URLs"""
    MEDIA_TYPE_CHOICES = [
        ('image', _('Image')),
        ('video', _('Video')),
        ('audio', _('Audio')),
        ('document', _('Document')),
    ]
    
    original_url = models.URLField()
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES)
    media_file = models.FileField(upload_to='downloaded_media/%Y/%m/%d/')
    title = models.CharField(max_length=300, blank=True)
    file_size = models.BigIntegerField()  # in bytes
    downloaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-downloaded_at']
    
    def __str__(self):
        return f"{self.media_type} - {self.title or self.original_url}"
