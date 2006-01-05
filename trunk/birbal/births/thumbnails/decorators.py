def debug(obj, msg, *args):
    import sys
    print >>sys.stderr, '[%s] %s' % (obj.__class__.__name__, (msg % args))
#

def thumbnail_cleanup(post_delete=None):
    def new_post_delete(self):
        from thumbnails.utils import remove_thumbnails
        from django.core.meta.fields import ImageField
        for obj in self._meta.fields:
            if isinstance(obj, ImageField):
                url = getattr(self, 'get_%s_url' % obj.name)()
                remove_thumbnails(url)
        #
        if post_delete:
            post_delete(self)
    #
    
    return new_post_delete
#
