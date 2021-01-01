from django.shortcuts import render, redirect
from .models import Certificate
from .forms import ContactForm
from django.core.mail import send_mail


def about(request):
    name = ''
    email = ''
    message = ''
    form = ContactForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data.get("name")
        email = form.cleaned_data.get("email")
        message = form.cleaned_data.get("message")\

        subject = "An email from my blog."

        message = name + " with the email, " + email + \
            ", sent the following message:\n\n" + message
        send_mail(subject, message, 'teertha.d87@gmail.com', ['teertha.d87@gmail.com'],
                  fail_silently=False)

        context = {
            'certificates': Certificate.objects.all(),
            'form': form,
        }
        return render(request, 'portfolio/about.html', context)

    else:
        context = {
            'certificates': Certificate.objects.all(),
            'form': form,
        }
        return render(request, 'portfolio/about.html', context)

def mypage(request):
    return render(request, 'mypage.html', {})