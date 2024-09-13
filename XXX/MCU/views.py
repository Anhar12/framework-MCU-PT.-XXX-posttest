from django.shortcuts import render

# Create your views here.
def Home(request):
    context = {
        'home' : True
    }
    return render(request, 'MCU/index.html', context)

def About(request):
    context = {
        'about' : True
    }
    return render(request, 'MCU/about.html', context)

def Contact(request):
    context = {
        'contact' : True
    }
    return render(request, 'MCU/contact.html', context)
