from django.db import models
from django.utils.translation import gettext_lazy as _


class MediaCategory(models.Model):
    """Categories for downloaded media"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Media Categories"
    
    def __str__(self):
        return self.name


class StoredMedia(models.Model):
    """Stored media files downloaded from external URLs"""
    MEDIA_TYPE_CHOICES = [
        ('image', _('Image')),
        ('video', _('Video')),
        ('audio', _('Audio')),
        ('document', _('Document')),
    ]
    
    original_url = models.URLField()
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES)
    media_file = models.FileField(upload_to='media/%Y/%m/%d/')
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        MediaCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='media'
    )
    file_size = models.BigIntegerField()  # in bytes
    duration = models.IntegerField(null=True, blank=True)  # in seconds, for audio/video
    download_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', _('Pending')),
            ('downloading', _('Downloading')),
            ('completed', _('Completed')),
            ('failed', _('Failed')),
        ],
        default='pending'
    )
    error_message = models.TextField(blank=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-downloaded_at']
        verbose_name_plural = "Stored Media"
    
    def __str__(self):
        return f"{self.title} ({self.media_type})"
