from django.urls import path

from kaf_pas.planing.views import operation_section

urlpatterns = [

    path('Operation_section/Fetch/', operation_section.Operation_section_Fetch),
    path('Operation_section/Add', operation_section.Operation_section_Add),
    path('Operation_section/Update', operation_section.Operation_section_Update),
    path('Operation_section/Remove', operation_section.Operation_section_Remove),
    path('Operation_section/Lookup/', operation_section.Operation_section_Lookup),
    path('Operation_section/Info/', operation_section.Operation_section_Info),
    path('Operation_section/Copy', operation_section.Operation_section_Copy),

]
