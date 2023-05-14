from django.urls import path

from . import views

urlpatterns = [
    path('register/' ,views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/' ,views.logoutUser, name='logout'),
    path("offer-filter", views.FilterView.as_view(), name="filter-page"),
    path("add-offer", views.add_offer, name="user-add-offer"),
    path("my-offers", views.user_offer_list, name="user-offer-list"),
    path("", views.index, name="index"),
]