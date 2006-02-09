# -*- coding: iso-8859-1 -*-
from django.core import template_loader
from django.core.extensions import DjangoContext as Context
from django.parts.auth.formfields import AuthenticationForm
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



class LoginManipulator(AuthenticationForm):
    def __init__(self, request):
        AuthenticationForm.__init__(self, request)
        self.fields.append(
            formfields.CheckboxField(field_name="remember"))

def index(request):
    manipulator = LoginManipulator(request)
    redirect_to = request.REQUEST.get('next','')
    if request.POST:
        new_data = request.POST.copy()
        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            request.session[users.SESSION_KEY] = manipulator.get_user_id()
            request.session.delete_test_cookie()
            if request.REQUEST.has_key('next'):
                return HttpResponseRedirect(request.REQUEST['next'])
            else:
                return HttpResponseRedirect("../home/")
    else:
        request.session.set_test_cookie()
        errors = new_data = {}

    form = formfields.FormWrapper(manipulator, new_data, errors)
    return render_to_response('myapp/index',
                              {'form': form,
                               'signin_page': True,
                               'redirect_to': redirect_to},
                              context_instance=DjangoContext(request))



