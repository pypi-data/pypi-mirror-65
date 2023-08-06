from django.urls import path

from kaf_pas.ckk.views import item_qty

urlpatterns = [

    path('Item_qty/Fetch/', item_qty.Item_qty_Fetch),
    path('Item_qty/Add', item_qty.Item_qty_Add),
    path('Item_qty/Update', item_qty.Item_qty_Update),
    path('Item_qty/Remove', item_qty.Item_qty_Remove),
    path('Item_qty/Lookup/', item_qty.Item_qty_Lookup),
    path('Item_qty/Info/', item_qty.Item_qty_Info),
    path('Item_qty/Copy', item_qty.Item_qty_Copy),

]
