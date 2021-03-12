from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from main.sitemaps import PostSiteMap

sitemaps = {
    'posts': PostSiteMap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('main.urls', namespace='main')),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='from django.contrib.sitemaps.views.sitemap'
    )
]
