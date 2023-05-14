from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView

from main.models import Offert
from main.filters import OfferFilter

def index(request):
    return HttpResponseRedirect(redirect_to='offer-filter')

# def offer_filter(response):
#     offers = Offert.objects.all()
#     for offer in offers:
#         if offer.locations:
#             offer.locations = offer.locations.split(", ") 
#     filter_form = OfferFilter()
#     context ={'offers' : offers, 
#               'form': filter_form.form} 
#     return render(response, "main/filter_page.html", context)

class FilterView(ListView):
    queryset = Offert.objects.all()
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
        self.__repair_locations(context['offers'])
        return context
    
    def __repair_locations(self, queryset):
        for offer in queryset:
            if offer.locations:
                offer.locations = offer.locations.split(", ") 
