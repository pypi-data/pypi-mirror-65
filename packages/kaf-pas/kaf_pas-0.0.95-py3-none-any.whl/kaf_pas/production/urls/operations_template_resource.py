from django.urls import path

from kaf_pas.production.views import operations_template_resource

urlpatterns = [

    path('Operations_template_resource/Fetch/', operations_template_resource.Operations_template_resource_Fetch),
    path('Operations_template_resource/Add', operations_template_resource.Operations_template_resource_Add),
    path('Operations_template_resource/Update', operations_template_resource.Operations_template_resource_Update),
    path('Operations_template_resource/Remove', operations_template_resource.Operations_template_resource_Remove),
    path('Operations_template_resource/Lookup/', operations_template_resource.Operations_template_resource_Lookup),
    path('Operations_template_resource/Info/', operations_template_resource.Operations_template_resource_Info),
    path('Operations_template_resource/Copy', operations_template_resource.Operations_template_resource_Copy),

]
