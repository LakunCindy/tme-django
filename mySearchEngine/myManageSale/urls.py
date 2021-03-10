from django.urls import path
from myManageSale import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('putonsale/<int:id>/<int:newprice>/', views.UpdateSaleProductDetail.as_view()),
    path('removesale/<int:id>',views.DeleteSaleProductDetail.as_view())
]   