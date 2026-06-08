from django.contrib.sitemaps import Sitemap
from .models import Post, Project


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, item):
        return item.updated_at
    
    def location(self, item):
        return item.get_absolute_url()


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Project.objects.all()

    def lastmod(self, item):
        return item.updated_at
    
    def location(self, item):
        return f'/projects/{item.slug}/'
