from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from django.utils.translation import activate

# generic view that renders the landing_page.html 

def landing_page(request):
    activate('es')
    context = {

    }
    resp = render(request, 'grand_prix/landing_page.html', context)
    return resp
