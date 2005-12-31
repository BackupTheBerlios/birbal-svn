from django.core import template_loader
from django.core.extensions import DjangoContext as Context
from django.utils.httpwrappers import HttpResponse
from births.apps.register.models.register import *
import datetime
from django.core.exceptions import Http404
from births.apps.website.views import menu_items,extract



def dutyroster(request):
    """ Shows attendance status for employees
        """
    list = persons.get_list()
    t = template_loader.get_template('register/officials')
    c = Context(request,
                {'list':list,
                 'ads':extract(),
                 'mn': menu_items,
                 })
    
    return HttpResponse(t.render(c))


