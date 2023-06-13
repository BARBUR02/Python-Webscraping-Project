from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login,logout

from .forms import OfferForm, RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required

from main.models import Offert, Announcement, CustomUser
from main.filters import OfferFilter


def repair_locations(queryset):
        for offer in queryset:
            if offer.locations:
                offer.locations = offer.locations.split(", ") 

# def calculate_range(queryset):
#     min = 10000 
#     max = 0
#     for offer in queryset:
#         if offer.minPrice < min:
#             min = offer.minPrice
#         if offer.minPrice > max:
#             max = offer.minPrice
#     return min, max

def registerUser(request):
    user = request.user
    if user.is_authenticated:
        return redirect('filter-page')
    context = {}
    if request.POST:
        # print("RECEIVED POST!!")
        form = RegistrationForm(request.POST)
        # print(f'FORM: {form}')
        # print(f'Form is valid: {form.is_valid()}')
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
        # print(f"LOGIN, valid form: { form.is_valid()}, value: {form.cleaned_data}, form:{form} ")
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
    context_object_name ='offers'
    template_name='main/filter_page.html'
    paginate_by=20

    def get_queryset(self):
        queryset = super().get_queryset()  
        self.filterset = OfferFilter(self.request.GET, queryset=queryset)
        if 'test' in self.request.GET:
            print("IN")
        else: 
            print("OUT")
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['form'] = self.filterset.form
        repair_locations(context['offers'])
        # minRange, maxRange = calculate_range(context['offers']) #liczy tylko dla strony, którą aktualnie wyświetla
        # context['minRange'] = minRange
        # context['maxRange'] = maxRange 
        return context


# user specific views:
@login_required(login_url="/login/")
def add_offer(request):
    user = request.user
    context = {}
    context['user'] = user
    if not user.is_authenticated:
        return redirect('filter-page')
    if request.POST:
        form = OfferForm(request.POST, request.FILES)
        # print(f"Valid form: { form.is_valid()}, value: {form.cleaned_data}")
        if form.is_valid():
            ai = user.id
            a = Announcement(**form.cleaned_data, maxPrice=form.cleaned_data['minPrice'], author_id=ai, from_our_user=True)
            a.save() 
            return redirect('user-offer-list')           
        else:
            context['offer_form'] = form
    return render(request, 'main/offer_add.html', context)


@login_required(login_url="/login/")
def user_offer_list(request):
    user = request.user
    context = {}    
    context["offers"] = Announcement.objects.filter(author_id=user.id)
    repair_locations(context['offers'])
    
    if request.POST:
        Announcement.objects.get(id=request.POST.get('delete')).delete()
        context["offers"] = Announcement.objects.filter(author_id=user.id)
        repair_locations(context['offers'])
        return render(request, 'main/offer_list.html', context=context)
    return render(request, 'main/offer_list.html', context=context)


@login_required(login_url="/login/")
def user_offer_edit(request, offerId):
    announcement = Announcement.objects.filter(id=offerId).first()
    if not announcement: 
        return HttpResponse("Given id does not exist")
    if not announcement.author_id == request.user.id:
        return HttpResponse("No permissions to this offer")

    if request.POST:
        form = OfferForm(request.POST)
        print(form.is_valid())
        print(form.cleaned_data)
        data = form.cleaned_data
        # announcement.update(**data)
        Announcement.objects.filter(id=offerId).update(**data, maxPrice=data["minPrice"])
        return redirect('user-offer-list')
    context = {
        "offer": announcement
    }
    return render(request, 'main/offer_edit.html', context=context)

def offer(request, offerId):
    announcement = Announcement.objects.filter(id=offerId).first()
    user = CustomUser.objects.filter(id=announcement.author_id).first()
    number_hidden = True
    if not announcement: 
        return HttpResponse("Nie ma takiej oferty")
    
    announcement.offer_check += 1
    announcement.save()
    
    if request.method == 'POST':
        number_hidden = False
        announcement.phone_check += 1
        announcement.offer_check -= 1
        announcement.save()

    context = {
        "offer": announcement,
        "user": user,
        "number_hidden": number_hidden
    }

    return render(request, 'main/offer.html', context=context)