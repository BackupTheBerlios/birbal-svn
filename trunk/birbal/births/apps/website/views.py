from django.core import template_loader
from django.core.extensions import DjangoContext as Context
from django.utils.httpwrappers import HttpResponse
from births.apps.website.models.website import *
import datetime
from django.core.exceptions import Http404


menu_items = [
              {'name':'Home','url':'fac/HM/','id':''},
              {'name':'FAQ','url':'fac/FQ/','id':''},
              {'name':'Documents','url':'fac/DC/','id':''},
              {'name':'Gallery','url':'galls//','id':''},
              ]

fac_types ={
    'HM': 'Home',
    'FQ': 'Faq',
    'DC': 'Documentation',
    'AM': 'Amenities'
    }


        

def extract():
    """ Gets the advertisements and announcements for the
        right column
        """
    list = advertisements.get_values(fields=['title','id'],
                              expires__gt=datetime.datetime.now(),
                           order_by=('-date',),
                              limit=5)
    return list




def index(request):
    """ Not used
        """
    t = template_loader.get_template('register/index')
    c = Context(request,
                {'ads':extract(),
                 'mn': menu_items,
                 })
    
    return HttpResponse(t.render(c))

def fac(request,type):
    """ View for display of the documentation
        generates all pages on the fly
        """
    list = facilitys.get_list(type__exact=type,)
    t = template_loader.get_template('register/fac')
    c = Context(request,
                {'list':list,'tp':type,
                 'ads':extract(),
                 'mn': menu_items,
                 })
    
    return HttpResponse(t.render(c))



def gallall(request,gall=''):
    """ View for display of the thumbnails
        in the gallery
        """
    if gall:
        list = photos.get_list(tag__id__exact=gall)
    else:
        list = []
    gals = tags.get_list()
    gal = tags.get_object(id__exact=gall)
    t = template_loader.get_template('website/gallall')
    c = Context(request,
                {'list':list,
                 'ads':extract(),
                 'mn': menu_items,
                 'gals':gals,
                 'gal':gal,
                 })
    return HttpResponse(t.render(c))

def gal(request,id):
    """ View for display of the thumbnails
        in the gallery
        """
    list = photos.get_list(pk=id)
    gals = tags.get_list()
    t = template_loader.get_template('website/gal')
    c = Context(request,
                {'list':list,
                 'ads':extract(),
                 'mn': menu_items,
                 'gals':gals,
                 
                 })
    return HttpResponse(t.render(c))


