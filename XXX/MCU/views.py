from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Regis, Users, Result
from django.core import serializers
from django.utils.dateparse import parse_date
from django.db.models import Q
from .decorators import group_required
from datetime import date as dt_date
import json

def Home(request):
    context = {
        'section' : 'home'
    }
    return render(request, 'Home/index.html', context)

def About(request):
    context = {
        'section' : 'about'
    }
    return render(request, 'Home/about.html', context)

def Contact(request):
    context = {
        'section' : 'contact'
    }
    return render(request, 'Home/contact.html', context)

def SignIn(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    context = {
        'section' : 'signIn'
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': 'success',
                'message': 'Login successful!',
                'role' : user.role,
                'isAdmin' : user.is_staff
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Login failed! Please check your credentials.',
                'errors': {
                    'login': ['Invalid email or password.']
                }
            })

    return render(request, 'Home/signIn.html', context)

def SignUp(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Registration successful!'
            })
        else:
            errors = {}
            for field, messages in form.errors.items():
                errors[field] = messages

            print(errors)   
            return JsonResponse({
                'status': 'error',
                'message': 'Registration failed! Please check your input.',
                'errors': errors
            })

    else:
        form = SignUpForm()
    return render(request, 'Home/signUp.html', {'form': form, 'section' : 'signIn'})

def SignOut(request):
    logout(request)
    return redirect('signIn') 

@login_required
def Dashboard(request):
    if request.user.role == Users.USER and not request.user.is_superuser:
        return redirect('UserDashboard')
    elif request.user.role == Users.DOCTOR and not request.user.is_superuser:
        return redirect('DoctorDashboard')
    elif request.user.is_superuser:
        return redirect('UserDashboard')
    return HttpResponseForbidden("You do not have permission to access this page.")

@login_required
@group_required(Users.USER)
def UserDashboard(request):
    regis_data = Regis.objects.filter(id_user=request.user, is_done=False).order_by('date', 'no_antrean')
    query = request.GET.get('q')
    if query:
        regis_data = Regis.objects.filter(Q(id_user=request.user) & (Q(date__icontains=query) | Q(no_antrean__icontains=query))).order_by('date', 'no_antrean')
    
    regis_json = serializers.serialize('json', regis_data)

    context = {
        'section': 'dashboard',
        'user': request.user,
        'role': request.user.role,
        'regis_data': regis_json,
        'query': query
    }

    return render(request, 'MCU/dashboard.html', context)

@require_POST
@login_required
@group_required(Users.USER)
def deleteRegis(request):
    if request.user.role != Users.USER or request.user.is_superuser:
        return redirect('signIn')
    
    try:
        body = json.loads(request.body)
        regis_id = body.get('regis_id')
        print(regis_id)
        Regis.objects.get(id=regis_id).delete()
        return JsonResponse({'success': True, 'message': 'Registration deleted successfully.'})
    except Regis.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Registration not found.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@require_POST
@login_required
@group_required(Users.USER)
def regisMCU(request):
    try:
        data = json.loads(request.body)
        date_str = data.get('date')

        if not date_str:
            return JsonResponse({'success': False, 'message': 'Date is required.'})

        date = parse_date(date_str)
        if not date:
            return JsonResponse({'success': False, 'message': 'Invalid date format.'})

        if date <= dt_date.today():
            return JsonResponse({'success': False, 'message': 'Date must be in the future, at least 1 day from today.'})
        
        registration = Regis.objects.create(id_user=request.user, date=date)

        return JsonResponse({
            'success': True,
            'message': 'Registration successful!',
            'regis_id': registration.id,
            'date': registration.date.strftime('%Y-%m-%d'),
            'no_antrean': registration.no_antrean,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@require_POST
@login_required
@group_required(Users.USER)
def updateRegis(request):
    try:
        data = json.loads(request.body)
        date_str = data.get('date')
        id = data.get('regis_id')

        if not date_str:
            return JsonResponse({'success': False, 'message': 'Date is required.'})

        date = parse_date(date_str)
        if not date:
            return JsonResponse({'success': False, 'message': 'Invalid date format.'})

        registration = Regis.objects.get(id=id)
        registration.date =date
        registration.save()

        return JsonResponse({
            'success': True,
            'message': 'Update successful!',
            'regis_id': registration.id,
            'date': registration.date.strftime('%Y-%m-%d'),
            'no_antrean': registration.no_antrean,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
@login_required
@group_required(Users.USER)
def UserHistory(request):
    history_data = Result.objects.filter(id_mcu_regis__id_user=request.user).order_by('date')
    query = request.GET.get('q')
    if query:
        history_data = Result.objects.filter(
            Q(id_mcu_regis__id_user=request.user) & (
                Q(date__icontains=query) | 
                Q(id_doctor__first_name__icontains=query) | 
                Q(id_doctor__last_name__icontains=query) | 
                Q(result__icontains=query) | 
                Q(notes__icontains=query) | 
                Q(no_document__icontains=query)
            )
        ).order_by('date')
    
    formatted_history_data = []
    for data in history_data:
        formatted_history_data.append({
            'pk': data.pk,
            'date': data.date.strftime('%Y-%m-%d'),
            'doctor': data.id_doctor.first_name + ' ' + data.id_doctor.last_name,
            'result': data.result,
            'notes': data.notes,
            'document': data.no_document,
        })

    history_json = json.dumps(formatted_history_data)

    context = {
        'section': 'history',
        'user': request.user,
        'role': request.user.role,
        'history_data': history_json,
        'query': query
    }

    return render(request, 'MCU/history.html', context)

@login_required
@group_required(Users.DOCTOR)
def DoctorDashboard(request):
    regis_data = Regis.objects.filter(is_done=False).order_by('date', 'no_antrean')
    query = request.GET.get('q')
    if query:
        regis_data = Regis.objects.filter(Q(date__icontains=query) | Q(no_antrean__icontains=query)).order_by('date', 'no_antrean')
    
    formatted_regis_data = []
    for data in regis_data:
        formatted_regis_data.append({
            'pk': data.pk,
            'name': data.id_user.first_name + ' ' + data.id_user.last_name,
            'date': data.date.strftime('%Y-%m-%d'),
            'no_antrean': data.no_antrean
        })

    regis_json = json.dumps(formatted_regis_data)

    context = {
        'section': 'dashboard',
        'user': request.user,
        'role': request.user.role,
        'regis_data': regis_json,
        'query': query
    }
    
    return render(request, 'Doctor/dashboard.html', context)

@login_required
@group_required(Users.DOCTOR)
def DoctorHistory(request):
    history_data = Result.objects.filter(id_doctor=request.user).order_by('date')
    query = request.GET.get('q')
    if query:
        history_data = Result.objects.filter(
            Q(date__icontains=query) | 
            Q(id_mcu_regis__id_user__first_name__icontains=query) | 
            Q(id_mcu_regis__id_user__last_name__icontains=query) | 
            Q(result__icontains=query) | 
            Q(notes__icontains=query) | 
            Q(no_document__icontains=query)
        ).order_by('date')
    
    formatted_history_data = []
    for data in history_data:
        formatted_history_data.append({
            'pk': data.pk,
            'date': data.date.strftime('%Y-%m-%d'),
            'name': data.id_mcu_regis.id_user.first_name + ' ' + data.id_mcu_regis.id_user.last_name,
            'result': data.result,
            'notes': data.notes,
            'document': data.no_document,
            'conclusion': data.conclusion
        })

    history_json = json.dumps(formatted_history_data)

    context = {
        'section': 'history',
        'user': request.user,
        'role': request.user.role,
        'history_data': history_json,
        'query': query
    }

    return render(request, 'Doctor/history.html', context)

@require_POST
@login_required
@group_required(Users.DOCTOR)
def finishMCU(request):
    try:
        data = json.loads(request.body)
        result = data.get('result')
        notes = data.get('notes')

        if not result or result not in [Result.P1, Result.P2, Result.P3, Result.P4, Result.P5, Result.P6, Result.P7]:
            return JsonResponse({'success': False, 'message': 'Result is required.'})

        registration = Regis.objects.get(id=data.get('regis_id'))
        
        if not registration:
            return JsonResponse({'success': False, 'message': 'Registration not found.'})
        
        result_obj = Result.objects.create(id_mcu_regis=registration, id_doctor=request.user, result=result, notes=notes)

        return JsonResponse({
            'success': True,
            'message': 'Done! MCU for' + result_obj.id_mcu_regis.id_user.first_name + ' ' + result_obj.id_mcu_regis.id_user.last_name + ' is finished.',
            'regis_id': result_obj.id_mcu_regis.id
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
@require_POST
@login_required
@group_required(Users.DOCTOR)
def updateMCU(request):
    try:
        data = json.loads(request.body)
        result = data.get('result')
        notes = data.get('notes')
        id = data.get('result_id')

        if not result or result not in [Result.P1, Result.P2, Result.P3, Result.P4, Result.P5, Result.P6, Result.P7]:
            return JsonResponse({'success': False, 'message': 'Result is required.'})

        result_obj = Result.objects.get(id=id)
        
        if not result_obj:
            return JsonResponse({'success': False, 'message': 'Result not found.'})

        result_obj.result = result
        result_obj.notes = notes
        result_obj.save()

        return JsonResponse({
            'success': True,
            'message': 'Update successful!',
            'pk': result_obj.id,
            'date': result_obj.date.strftime('%Y-%m-%d'),
            'name': result_obj.id_mcu_regis.id_user.first_name + ' ' + result_obj.id_mcu_regis.id_user.last_name,
            'result': result_obj.result,
            'notes': result_obj.notes,
            'document': result_obj.no_document,
            'conclusion': result_obj.conclusion
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})