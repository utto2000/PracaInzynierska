import math

from django.db.models import Max, Min
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from CloudOnSite.models import *
from CloudOnSite.forms import RegistrationForm, LoginForm


def home(request):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        return render(request, 'home.html')


def register(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')

                user = form.save()

                user.email = email
                user.save()
                return redirect('login')

        else:
            form = RegistrationForm()
        return render(request, 'register.html', {'form': form})
    else:
        return render(request, 'home.html')


def log_in(request):
    error_messages = {
        'invalid_login': "Please enter a correct %(username)s and password.",
        'inactive': "This account is inactive.",
    }

    if request.user.is_anonymous:
        if request.method == "POST":
            form = LoginForm(request.POST)
            print(form.error_messages)

            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.errors['Problem with login: '] = 'Check if you use correct username and password'
        else:
            form = LoginForm()
    else:
        return render(request, 'home.html')
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


def storage_view(request):
    user = request.user
    if user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.storage = True
        profile.save()

    return render(request, 'storage.html')

def storage_view_final(request):
    user = request.user
    if user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.storage = True
        profile.save()
        if request.method == 'POST':
            disks = request.POST.get('disks')
            storage = request.POST.get('storage')
            ram = request.POST.get('ram')
            ram_type = request.POST.get('ram_type')
            processors = request.POST.get('processors')
            raid = request.POST.get('raid')


        if storage != '10tb':
                if disks == '2_5':
                    available_disks = StorageShelf.objects.filter(disks2_5__gt=0)
                    min_price_disks = available_disks.aggregate(min_price=Min('price'))['min_price']
                    max_price_disks = available_disks.aggregate(max_price=Max('price'))['max_price']
                    slots_number_cheep = available_disks.filter(price__exact=min_price_disks).first().disks2_5
                    slots_number_expensive = available_disks.filter(price__exact=max_price_disks).first().disks2_5
                else:
                    available_disks = StorageShelf.objects.filter(disks3_5__gt=0)
                    min_price_disks = available_disks.aggregate(min_price=Min('price'))['min_price']
                    max_price_disks = available_disks.aggregate(max_price=Max('price'))['max_price']
                    slots_number_cheep = available_disks.filter(price__exact=min_price_disks).first().disks3_5
                    slots_number_expensive = available_disks.filter(price__exact=max_price_disks).first().disks3_5

                if storage == '10pb':
                    terabites = 10000
                elif storage == '1pb':
                    terabites = 1000
                elif storage == '100pb':
                    terabites =100000
                needed_shelf_most_expensive = math.ceil(terabites / (12 * slots_number_expensive))
                needed_shelf_most_cheep = math.ceil(terabites / (12 * slots_number_cheep))


        if ram_type == 'lowend':
                dbram_type = StorageRam.objects.filter(price__lt=220)
        elif ram_type == 'highend':
                dbram_type = StorageRam.objects.filter(price__gt=379)
        else:
                dbram_type = StorageRam.objects.filter(price__lt=380, price__gt=219)

        min_price_ram = dbram_type.aggregate(min_price=Min('price'))['min_price']
        max_price_ram = dbram_type.aggregate(max_price=Max('price'))['max_price']
        ram_capacity_cheep = dbram_type.filter(price__exact=min_price_ram).first().size
        ram_capacity_expenisve = dbram_type.filter(price__exact=max_price_ram).first().size
        if ram == '100':
            how_many_rams_cheep = 100 / ram_capacity_cheep
            how_many_rams_expensive = 100 / ram_capacity_expenisve
        elif ram == '200':
            how_many_rams_cheep = 200 / ram_capacity_cheep
            how_many_rams_expensive = 200 / ram_capacity_expenisve
        elif ram == '300':
            how_many_rams_cheep = 300 / ram_capacity_cheep
            how_many_rams_expensive = 300 / ram_capacity_expenisve


        if processors == 'lowend':
                processors_type = StorageProc.objects.filter(price__lt=1001)
        elif processors == 'highend':
                processors_type = StorageProc.objects.filter(price__gt=2499)
        else:
                processors_type = StorageProc.objects.filter(price__lt=2500, price__gt=1000)
        min_price_proc = processors_type.aggregate(min_price=Min('price'))['min_price']
        max_price_proc = processors_type.aggregate(max_price=Max('price'))['max_price']

        if raid == '5':
            price_of_disks = 500 * math.ceil(((terabites/12) + 1))
        elif raid == '6':
            price_of_disks = 500 * math.ceil(((terabites / 12) + 2))
        servers = StorageServer.objects.all()
        min_server = servers.aggregate(min_price=Min('price'))['min_price']
        max_server = servers.aggregate(max_price=Max('price'))['max_price']
        min_price = price_of_disks + min_price_proc + min_price_ram + min_price_disks + min_server
        max_price = price_of_disks + max_price_proc + max_price_ram + max_price_disks + max_server
        print('min_price', min_price)
        print('max_price', max_price)

        context = {
            'available_disks': available_disks,
            'needed_shelf_most_expensive': needed_shelf_most_expensive,
            'needed_shelf_most_cheep': needed_shelf_most_cheep,
            'dbram_type': dbram_type,
            'raid_type': raid,
            'min_price': min_price,
            'max_price': max_price,
            'servers': servers,
            'ram_type': dbram_type,
            'price_rams_cheep' : how_many_rams_cheep * min_price_ram,
            'price_rams_expensive': how_many_rams_expensive * max_price_ram,
            'how_many_rams_cheep': how_many_rams_cheep,
            'how_many_rams_expensive': how_many_rams_expensive,

        }
        return render()

def profile_view(request):
    user = request.user
    if user.is_authenticated:
        try:
            profile, created = UserProfile.objects.get_or_create(user=user)
        except UserProfile.DoesNotExist:
            profile = None
        return render(request, 'profile.html', {'profile': profile})
    else:
        return redirect('login')
