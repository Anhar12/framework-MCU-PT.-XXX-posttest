from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Users
from django.contrib.auth.hashers import make_password
import json

# Views Controller
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

def DashboardDoctor(request):
    user_role = request.session.get('user_role', None)

    if user_role is None:
        return redirect('request_rejected') 

    if user_role != 1:
        return redirect('request_rejected')
    
    context = {
        'DashboardDoctor' : True
    }
    return render(request, 'MCU/DashboardDoctor.html', context)

def DashboardUser(request):
    user_role = request.session.get('user_role', None)

    if user_role is None:
        return redirect('request_rejected') 

    if not user_role != 2:
        return redirect('request_rejected')

    context = {
        'DashboardUser': True
    }
    return render(request, 'MCU/DashboardUser.html', context)

def RequestRejected(request):
    return render(request, 'MCU/rejected.html')

def Belum(request):
    return render(request, 'MCU/belum.html')

def DoctorManagement(request):
    is_staff = request.session.get('is_staff', None)

    if is_staff is None:
        return redirect('request_rejected') 

    if not is_staff:
        return redirect('request_rejected')

    context = {
        'DoctorManagement': True
    }
    return render(request, 'MCU/DoctorManagement.html', context)

# API Controller
def SignOut(request):
    request.session.flush()
    return redirect('portal')

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

def CreateDoctor(request):
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
                password=make_password(password),
                role=1
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
            request.session['is_staff'] = user.is_staff
            request.session.save()
            
            # if user.role == 1:
            #     return redirect('dashboard_doctor')
            # elif user.role == 2:
            #     return redirect('dashboard_user')
            return JsonResponse({
                'success': 'Logged in successfully',
                'role': user.role,
                'is_staff': user.is_staff,
            }, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)