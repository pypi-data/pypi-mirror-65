from django.urls import path

from kaf_pas.planing.views import production_order_values

urlpatterns = [

    path('Production_order_values/Fetch/', production_order_values.Production_order_values_Fetch),
    path('Production_order_values/Add', production_order_values.Production_order_values_Add),
    path('Production_order_values/Update', production_order_values.Production_order_values_Update),
    path('Production_order_values/Remove', production_order_values.Production_order_values_Remove),
    path('Production_order_values/Lookup/', production_order_values.Production_order_values_Lookup),
    path('Production_order_values/Info/', production_order_values.Production_order_values_Info),
    path('Production_order_values/Copy', production_order_values.Production_order_values_Copy),

]
