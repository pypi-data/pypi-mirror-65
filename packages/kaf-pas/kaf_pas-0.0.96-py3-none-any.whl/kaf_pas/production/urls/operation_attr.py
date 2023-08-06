from django.urls import path

from kaf_pas.production.views import operation_attr

urlpatterns = [

    path('Operation_attr/Fetch/', operation_attr.Operation_attr_Fetch),
    path('Operation_attr/Add', operation_attr.Operation_attr_Add),
    path('Operation_attr/Update', operation_attr.Operation_attr_Update),
    path('Operation_attr/Remove', operation_attr.Operation_attr_Remove),
    path('Operation_attr/Lookup/', operation_attr.Operation_attr_Lookup),
    path('Operation_attr/Info/', operation_attr.Operation_attr_Info),
    path('Operation_attr/Copy', operation_attr.Operation_attr_Copy),

]
