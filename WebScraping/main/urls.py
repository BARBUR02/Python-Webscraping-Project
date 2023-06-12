from django.urls import path

from . import views

urlpatterns = [
    path('register/' ,views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/' ,views.logoutUser, name='logout'),
    path("offer-filter", views.FilterView.as_view(), name="filter-page"),
    path('offer-filter/<int:offerId>', views.offer, name="offer"),
    path("add-offer", views.add_offer, name="user-add-offer"),
    path("my-offers/<int:offerId>", views.user_offer_edit, name="user-offer-edit"),
    path("my-offers", views.user_offer_list, name="user-offer-list"),
    path("", views.index, name="index"),
]