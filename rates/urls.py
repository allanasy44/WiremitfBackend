from django.urls import path
from .views import LatestRatesView, RateDetailView, HistoricalRatesView, AdminRefreshView
urlpatterns=[path('rates',LatestRatesView.as_view()), path('rates/<str:currency>',RateDetailView.as_view()), path('historical/rates',HistoricalRatesView.as_view()), path('admin/refresh',AdminRefreshView.as_view())]
