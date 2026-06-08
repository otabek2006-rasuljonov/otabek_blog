from django.contrib import admin
from .models import MediaCategory, StoredMedia


class MediaCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class StoredMediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'download_status', 'file_size', 'downloaded_at')
    list_filter = ('media_type', 'download_status', 'downloaded_at')
    search_fields = ('title', 'original_url', 'description')
    readonly_fields = ('file_size', 'downloaded_at', 'updated_at', 'original_url')
    fieldsets = (
        ('Media Info', {
            'fields': ('title', 'description', 'media_type', 'category')
        }),
        ('File', {
            'fields': ('original_url', 'media_file', 'file_size', 'duration')
        }),
        ('Status', {
            'fields': ('download_status', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('downloaded_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(MediaCategory, MediaCategoryAdmin)
admin.site.register(StoredMedia, StoredMediaAdmin)
