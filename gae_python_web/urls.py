from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
handler404 = 'app.views.error404'
handler500 = 'app.views.error500'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gae_python_web.views.home', name='home'),
    # url(r'^gae_python_web/', include('gae_python_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'app.views.home'),
    url(r'^customers/$', 'app.views.customers'),
    url(r'^customers/add/', 'app.views.customers_add'),
    url(r'^customers/delete/(?P<id>[\w]{16})/$', 'app.views.customers_delete'),
    url(r'^customers/modify/(?P<id>[\w]{16})$', 'app.views.customers_modify'),
)
