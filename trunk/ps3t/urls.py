from django.contrib import admin
from django.conf.urls.defaults import *
from ps3t import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^ps3t/', include('ps3t.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^rank/$', 'ps3t.myps3t.views.rank'),
    (r'^rank/(?P<userName>.{1,})/$', 'ps3t.myps3t.views.rankUser'),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.IMG_ROOT, 'show_indexes': True}),
    )

