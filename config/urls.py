from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.contrib.sitemaps.views import sitemap
from shop.sitemap import ProductSitemap
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.http import HttpResponseRedirect

sitemaps = {
    'products': ProductSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('shop.urls', 'config'), namespace='shop')),
    path('users/', include(('users.urls', 'config'), namespace='users')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('error/', TemplateView.as_view(template_name="error.html"), name='error'),
]

# Добавление маршрутов для обработки статических и медиа файлов при DEBUG = True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

# Перенаправление всех ненайденных URL на страницу ошибки (помещено в самый конец)
urlpatterns += [
    re_path(r'^.*$', lambda request: HttpResponseRedirect('/error/')),
]
