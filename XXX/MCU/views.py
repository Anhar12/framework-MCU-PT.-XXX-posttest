from django.shortcuts import render
from django.http import JsonResponse
from .models import Users
from django.contrib.auth.hashers import make_password
import json

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

def Portal(request):
    context = {
        'portal' : True
    }
    return render(request, 'MCU/portal.html', context)

def SignOut(request):
    return render(request)

def SignUp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            confirm_password = data.get('confirmPassword')
            agreement = data.get('agreement')

            if password != confirm_password:
                return JsonResponse({'error': 'Passwords do not match'}, status=400)

            if not agreement:
                return JsonResponse({'error': 'You must agree to the terms'}, status=400)

            if len(email) > 150:
                return JsonResponse({'error': 'Email exceeds maximum length of 150 characters'}, status=400)
            if len(username) > 150:
                return JsonResponse({'error': 'Username exceeds maximum length of 150 characters'}, status=400)

            if Users.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email is already in use'}, status=400)
            if Users.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username is already in use'}, status=400)

            user = Users(
                username=username,
                email=email,
                password=make_password(password)  # Enkripsi password
            )
            user.save()
            return JsonResponse({'success': 'User created successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def SignIn(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                return JsonResponse({'error': 'Invalid email or password'}, status=400)

            if not user.check_password(password):
                return JsonResponse({'error': 'Invalid email or password'}, status=400)

            request.session['user_id'] = user.id
            request.session['user_role'] = user.role
            request.session['user_username'] = user.username
            request.session['user_email'] = user.email
            
            return JsonResponse({'success': 'Logged in successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)