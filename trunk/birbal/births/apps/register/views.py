from django.core import template_loader
from django.core.extensions import DjangoContext as Context
from django.utils.httpwrappers import HttpResponse
from births.apps.register.models.register import advertisements
import datetime
from django.core.exceptions import Http404

menu_items = [
              {'name':'Home','url':'','id':''},
              {'name':'Mission','url':'mission/','id':''},
              {'name':'News','url':'news/NW/','id':''},
              
              ]


        

def extract():
    list = advertisements.get_values(fields=['title','id'],
                              expires__gt=datetime.datetime.now(),
                           order_by=('-date',),
                              limit=5)
    return list


def index(request):
    
    t = template_loader.get_template('register/index')
    c = Context(request,
                {'ads':extract(),
                 'mn': menu_items,
                 })
    
    return HttpResponse(t.render(c))


