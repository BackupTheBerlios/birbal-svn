from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^births/', include('births.apps.foo.urls.foo')),

    # Uncomment this for admin:
     (r'^births/admin/', include('django.contrib.admin.urls.admin')),
    (r'^births/$', 'births.apps.register.views.index'),
    (r'^births/ads/(?P<id>\d+)/$', 'births.apps.register.views.ads'),
    (r'^births/fac/(?P<type>\w+)/$', 'births.apps.register.views.fac'),
)
