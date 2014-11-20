from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_root.views.home', name='home'),
    # url(r'^django_root/', include('django_root.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^$', 'django_root.wl_app.index.index'),
    (r'^start_layout', 'django_root.wl_app.index.start_layout'),
    (r'^start_change', 'django_root.wl_app.index.start_change'),
)
