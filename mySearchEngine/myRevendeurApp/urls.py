from django.urls import path
from myRevendeurApp import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('infoproducts/', views.InfoStockProducts.as_view()),
    path('infoproduct/<int:pk>/', views.InfoStockProductDetail.as_view()),
    path('incrementStock/<int:id>/<int:number>/', views.IncrementStock.as_view()),
    path('decrementStock/<int:id>/<int:number>/', views.DecrementStock.as_view())
]   