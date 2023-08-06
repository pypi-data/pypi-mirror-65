from django.urls import path

from kaf_pas.planing.views import sections

urlpatterns = [

    path('Sections/Fetch/', sections.Sections_Fetch),
    path('Sections/Add', sections.Sections_Add),
    path('Sections/Update', sections.Sections_Update),
    path('Sections/Remove', sections.Sections_Remove),
    path('Sections/Lookup/', sections.Sections_Lookup),
    path('Sections/Info/', sections.Sections_Info),
    path('Sections/Copy', sections.Sections_Copy),

]
