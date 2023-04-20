from django.shortcuts import render

# generic view that renders the landing_page.html 

def landing_page(request):
    return render(request, 'landing_page.html')
