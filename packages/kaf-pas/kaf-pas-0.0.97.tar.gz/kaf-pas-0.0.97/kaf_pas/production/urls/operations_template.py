from django.urls import path

from kaf_pas.production.views import operations_template

urlpatterns = [

    path('Operations_template/Fetch/', operations_template.Operations_template_Fetch),
    path('Operations_template/Add', operations_template.Operations_template_Add),
    path('Operations_template/Update', operations_template.Operations_template_Update),
    path('Operations_template/Remove', operations_template.Operations_template_Remove),
    path('Operations_template/Lookup/', operations_template.Operations_template_Lookup),
    path('Operations_template/Info/', operations_template.Operations_template_Info),
    path('Operations_template/Copy', operations_template.Operations_template_Copy),

]
