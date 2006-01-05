from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^births/', include('births.apps.foo.urls.foo')),

    # Uncomment this for admin:
     (r'^births/admin/', include('django.contrib.admin.urls.admin')),
    (r'^births/$', 'births.apps.website.views.index'),
    (r'^births/galls/(?P<gall>\d*)/$', 'births.apps.website.views.gallall'),
    (r'^births/ads/(?P<id>\d+)/$', 'births.apps.website.views.ads'),
    (r'^births/fac/(?P<type>\w+)/$', 'births.apps.website.views.fac'),
    (r'^births/gal/(?P<id>\d+)/$', 'births.apps.website.views.gal'),
)
