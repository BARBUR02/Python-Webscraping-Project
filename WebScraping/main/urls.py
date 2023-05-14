from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("offer-filter", views.FilterView.as_view(), name="filter-page")
]