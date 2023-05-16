from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login,logout

from .forms import OfferForm, RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required

from main.models import Offert, Announcement
from main.filters import OfferFilter

from itertools import chain

def registerUser(request):
    user = request.user
    if user.is_authenticated:
        return redirect('filter-page')
    context = {}
    if request.POST:
        print("RECEIVED POST!!")
        form = RegistrationForm(request.POST)
        print(f'FORM: {form}')
        print(f'Form is valid: {form.is_valid()}')
        if form.is_valid():
            form.save()
            email =  form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1').lower()
            account = authenticate(email=email,password = raw_password)
            login(request,account)
            return  redirect('filter-page')
        else:
            context['registration_form'] = form 
            print(f'CONTEXT: {context}')

    return render(request, 'main/register.html', context=context)


def loginUser(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('filter-page')
    if request.POST:
        form = LoginForm(request.POST)
        print(f"LOGIN, valid form: { form.is_valid()}, value: {form.cleaned_data}, form:{form} ")
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)
            if user:
                login(request, user)
                return redirect('filter-page')
        else:
            context['login_form'] = form
    # context['login_form'] = None
    return render(request, 'main/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('filter-page')

def index(request):
    return redirect('filter-page')

class FilterView(ListView):
    queryset = Offert.objects.all()
    quesryset2 = Announcement.objects.all() #TODO to do zmiany, na szybko robiłem
    context_object_name ='offers'
    template_name='main/filter_page.html'
    paginate_by=20
            
    def get_queryset(self):
        queryset = super().get_queryset()   
        self.filterset = OfferFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['form'] = self.filterset.form
        context['our_offers'] = Announcement.objects.all()
        self.__repair_locations(context['offers'])
        return context
    
    def __repair_locations(self, queryset):
        for offer in queryset:
            if offer.locations:
                offer.locations = offer.locations.split(", ") 



# user specific views:
@login_required(login_url="/login/")
def add_offer(request):
    user = request.user
    context = {}
    context['user'] = user
    if not user.is_authenticated:
        return redirect('filter-page')
    if request.POST:
        form = OfferForm(request.POST)
        # print(f"LOGIN, valid form: { form.is_valid()}, value: {form.cleaned_data}")
        if form.is_valid():
            n = form.cleaned_data['name']
            s = form.cleaned_data['subject']
            l = form.cleaned_data['locations']
            p = form.cleaned_data['price']
            d = form.cleaned_data['description']
            ph = form.cleaned_data['phone_number']
            ai = user.id
            a = Announcement(name=n, subject=s, locations=l, price=p,
                             description=d, phone_number=ph, author_id=ai)
            a.save()            
        else:
            context['offer_form'] = form
    return render(request, 'main/offer_add.html', context)


@login_required(login_url="/login/")
def user_offer_list(request):
    user = request.user
    context = {}    
    context["offers"] = Announcement.objects.filter(author_id=user.id)
    for offer in context["offers"]:
        if offer.locations:
            offer.locations = offer.locations.split(", ") 
    
    if request.POST:
        print(request.POST)

    return render(request, 'main/offer_list.html', context=context)