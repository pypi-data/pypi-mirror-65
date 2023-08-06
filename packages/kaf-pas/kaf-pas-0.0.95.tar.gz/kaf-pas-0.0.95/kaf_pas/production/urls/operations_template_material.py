from django.urls import path

from kaf_pas.production.views import operations_template_material

urlpatterns = [

    path('Operations_template_material/Fetch/', operations_template_material.Operations_template_material_Fetch),
    path('Operations_template_material/Add', operations_template_material.Operations_template_material_Add),
    path('Operations_template_material/Update', operations_template_material.Operations_template_material_Update),
    path('Operations_template_material/Remove', operations_template_material.Operations_template_material_Remove),
    path('Operations_template_material/Lookup/', operations_template_material.Operations_template_material_Lookup),
    path('Operations_template_material/Info/', operations_template_material.Operations_template_material_Info),
    path('Operations_template_material/Copy', operations_template_material.Operations_template_material_Copy),

]
