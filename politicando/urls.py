from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'politicando.views.home', name='home'),
    # url(r'^politicando/', include('politicando.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r"^$", "core.views.home", name="home"),
    url(r"^quemsomos/$", "core.views.quemsomos", name="quemsomos"),
    url(r'^login/$', "django.contrib.auth.views.login",
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', "django.contrib.auth.views.logout",
        {'next_page': '/'}, name='logout'),
   # url(r'^promessaevida/', include("promessaevida.urls")),

    url(r'', include('social_auth.urls')),



)

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.STATIC_ROOT}),

        (r'^media/$', 'django.views.static.serve', 
        {'document_root': settings.MEDIA_ROOT}),
    )
