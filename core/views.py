from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse


class RobotsTxtView(TemplateView):
    """Robots.txt view for SEO"""
    template_name = 'robots.txt'
    content_type = 'text/plain'
    
    def get(self, request, *args, **kwargs):
        return HttpResponse(
            f"""User-agent: *
Allow: /

Sitemap: https://{request.get_host()}/sitemap.xml
""",
            content_type='text/plain'
        )

