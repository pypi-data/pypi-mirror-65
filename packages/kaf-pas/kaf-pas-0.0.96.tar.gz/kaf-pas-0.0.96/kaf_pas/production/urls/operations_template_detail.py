from django.urls import path

from kaf_pas.production.views import operations_template_detail

urlpatterns = [

    path('Operations_template_detail/Fetch/', operations_template_detail.Operations_template_detail_Fetch),
    path('Operations_template_detail/Add', operations_template_detail.Operations_template_detail_Add),
    path('Operations_template_detail/Update', operations_template_detail.Operations_template_detail_Update),
    path('Operations_template_detail/Remove', operations_template_detail.Operations_template_detail_Remove),
    path('Operations_template_detail/Lookup/', operations_template_detail.Operations_template_detail_Lookup),
    path('Operations_template_detail/Info/', operations_template_detail.Operations_template_detail_Info),
    path('Operations_template_detail/Copy', operations_template_detail.Operations_template_detail_Copy),
    path('Operations_template_detail/CopyOpers2Template', operations_template_detail.Operations_template_detail_CopyOpers),

]
