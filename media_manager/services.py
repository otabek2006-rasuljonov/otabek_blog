import os
import requests
from django.core.files.base import ContentFile
from django.utils import timezone
from .models import StoredMedia
import mimetypes
from urllib.parse import urlparse


class MediaDownloadService:
    """Service to download media files from URLs and store them locally"""
    
    MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
    ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    ALLOWED_VIDEO_TYPES = ['video/mp4', 'video/webm', 'video/ogg']
    ALLOWED_AUDIO_TYPES = ['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/webm']
    
    @staticmethod
    def get_media_type_from_mime(mime_type):
        """Determine media type from MIME type"""
        if mime_type in MediaDownloadService.ALLOWED_IMAGE_TYPES:
            return 'image'
        elif mime_type in MediaDownloadService.ALLOWED_VIDEO_TYPES:
            return 'video'
        elif mime_type in MediaDownloadService.ALLOWED_AUDIO_TYPES:
            return 'audio'
        elif mime_type.startswith('application/pdf') or mime_type.startswith('application/'):
            return 'document'
        return 'document'
    
    @staticmethod
    def download_media(url, title='', category=None, media_type=None):
        """Download media from URL and store it"""
        try:
            # Check if already exists
            existing = StoredMedia.objects.filter(original_url=url).first()
            if existing and existing.download_status == 'completed':
                return existing
            
            # Create or update media record
            media = StoredMedia.objects.filter(original_url=url).first()
            if not media:
                media = StoredMedia(
                    original_url=url,
                    title=title or urlparse(url).path.split('/')[-1],
                    category=category,
                    media_type=media_type or 'document',
                    download_status='downloading'
                )
            else:
                media.download_status = 'downloading'
            
            media.save()
            
            # Download file
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()
            
            # Check file size
            content_length = int(response.headers.get('Content-Length', 0))
            if content_length > MediaDownloadService.MAX_FILE_SIZE:
                raise Exception(f"File too large: {content_length} bytes")
            
            # Get MIME type
            content_type = response.headers.get('Content-Type', 'application/octet-stream').split(';')[0]
            if not media_type:
                media_type = MediaDownloadService.get_media_type_from_mime(content_type)
            
            # Get file extension
            ext = mimetypes.guess_extension(content_type) or '.bin'
            filename = f"{media.title}{ext}"
            
            # Download content
            file_content = b''
            for chunk in response.iter_content(chunk_size=8192):
                file_content += chunk
                if len(file_content) > MediaDownloadService.MAX_FILE_SIZE:
                    raise Exception("File exceeds maximum size")
            
            # Save to media object
            media.media_file.save(
                filename,
                ContentFile(file_content),
                save=False
            )
            media.file_size = len(file_content)
            media.media_type = media_type
            media.download_status = 'completed'
            media.error_message = ''
            media.save()
            
            return media
            
        except Exception as e:
            media.download_status = 'failed'
            media.error_message = str(e)
            media.save()
            raise
