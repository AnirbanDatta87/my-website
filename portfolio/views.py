from django.shortcuts import render
from .models import Certificate


def about(request):
    context = {
        'certificates': Certificate.objects.all()
    }
    return render(request, 'portfolio/about.html', context)
